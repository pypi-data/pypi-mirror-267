import logging
from datetime import datetime, timedelta
from enum import Enum
from http import HTTPMethod

import requests
from requests import Response

logger = logging.getLogger(f"{__name__}")


class APIVersion(Enum):
    VERSION_9 = 9


class EscoAPI:
    base_url: str
    username: str
    password: str
    client_id: str = ""
    version: APIVersion = APIVersion.VERSION_9

    __token: str = ""
    __expire_datetime: datetime

    def __make_request(
            self,
            request_endpoint: str,
            request_method: HTTPMethod,
            request_body: dict,
            error_message: str = ""
    ):
        req_call = getattr(requests, request_method.lower())
        headers = {
            "api-version": str(self.version.value)
        }
        if self.__token:
            headers["Authorization"] = f"Bearer {self.__token}"
        params = {
            "url": f"{self.base_url}{request_endpoint}",
            "json": request_body,
            "headers": headers
        }
        result: Response = req_call(**params)
        if 200 <= result.status_code <= 299:
            return result.json()
        else:
            if not error_message:
                error_message = f"Error during endpoint call: {request_endpoint}. Code: {result.status_code}"
            raise ConnectionRefusedError(error_message)

    def __esco_login(self):
        req_body = {
            "userName": self.username,
            "password": self.password,
            "clientId": self.client_id
        }

        result_data = self.__make_request(
            request_endpoint="/login",
            request_body=req_body,
            request_method=HTTPMethod.POST,
            error_message="Login to ESCO API failed."
        )

        self.__token = result_data["access_token"]
        expires_in_minutes = result_data["expires_in"] - 1
        self.__expire_datetime = datetime.now() + timedelta(minutes=expires_in_minutes)

    def __pre_connection(self):
        if datetime.now() > self.__expire_datetime:
            self.__esco_login()

    def __new__(cls, base_url: str, username: str, password: str, client_id: str, version: APIVersion):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EscoAPI, cls).__new__(cls)
        # noinspection PyUnresolvedReferences
        return cls.instance

    def __init__(
            self,
            base_url: str,
            username: str,
            password: str,
            client_id: str = "",
            version: APIVersion = APIVersion.VERSION_9
    ):
        """
        Initializes the EscoAPI client, starting a login to the platform.
        Instantiating a new EscoAPI client will not result in a new login (Singleton).
        Login runs automatically when the last token expires.
        :param base_url: The URL of your EscoAPI implementation. Include the protocol without slash at the end.
        :param username: The username of your EscoAPI client.
        :param password: The password of your EscoAPI client.
        :param client_id: Optional. Include if you want to specify a client_id.
        :param version: Optional. The EscoAPI version that you want to use. Default: Version 9.
        """
        self.base_url = f"{base_url}/api/v{version.value}"
        self.username = username
        self.password = password
        self.client_id = client_id
        self.version = version

        self.__esco_login()

    def get_posiciones(
            self,
            cuenta: str,
            por_concertacion: bool = True,
            es_consolidado: bool = False,
            incluir_monedas: bool = True,
            incluir_titulos: bool = False,
            incluir_opciones: bool = False,
            incluir_futuros: bool = False,
            incluir_fondos: bool = False,
            solo_saldos_iniciales: bool = True
    ):
        """
        Esta consulta devuelve las tenencias de instrumentos de una cuenta o una lista de cuentas a una fecha
        indicada y discrimina vencimientos de 24, 48hs y futuro. Las tenencias no se valúan generando una
        respuesta mas rapida de la consulta.
        :param cuenta: Cuenta comitente a consultar.
        :param por_concertacion: Indica si las tenencias se buscan por Fecha de Concertación o no.
        :param es_consolidado: Indica si se muestran todas las cuentas del usuario consolidadas o solo la cuenta seleccionada
        :param incluir_monedas: Indica si se incluyen tenencias de Monedas
        :param incluir_titulos: Indica si se incluyen tenencias de Titulos
        :param incluir_opciones: Indica si se incluyen tenencias de Opciones
        :param incluir_futuros: Indica si se incluyen tenencias de Futuros
        :param incluir_fondos: Indica si se incluyen tenencias de Fondos
        :param solo_saldos_iniciales: Indica si solo se muestran saldos al inicio del día o se impactan movimientos realizados en en el dia
        """
        req_body = {
          "cuentas": cuenta,
          "porConcertacion": por_concertacion,
          "esConsolidado": es_consolidado,
          "incluirMonedas": incluir_monedas,
          "incluirTitulos": incluir_titulos,
          "incluirOpciones": incluir_opciones,
          "incluirFuturos": incluir_futuros,
          "incluirFondos": incluir_fondos,
          "soloSaldosIniciales": solo_saldos_iniciales
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-posiciones",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_disponible_mon(
            self,
            cuenta: str,
            fecha_disponible: datetime = datetime.now(),
            moneda: str = "ARS",
            dias_rescates_pendientes: int = 0,
            dias_suscripciones_pendientes: int = 0,
            plazo: int = 0,
            incluye_creditos: bool = True,
            fecha_colocacion_hasta: datetime = datetime.now(),
            es_bloqueado_bcra: bool = False
    ):
        """
        Esta consulta informa el disponible de moneda para una cuenta comitente a una fecha determinada.
        La respuesta discrimina cómo se compone el saldo disponible.

        :param cuenta: Código de Comitente
        :param fecha_disponible: Fecha en que se pide la consulta
        :param moneda: Código ISO de la moneda
        :param dias_rescates_pendientes: Cantidad de días de antiguedad máximo para considerar Rescates pendientes de liquidación
        :param dias_suscripciones_pendientes: Cantidad de días de antiguedad máximo para considerar Suscripciones pendientes de liquidación.
        :param plazo: Plazo de liquidación del movimiento que se está cargando. Se suma al campo Fecha el plazo en días hábiles para calcular la fecha a la que se debe mostrar el disponible.
        :param incluye_creditos: Indica si se deben considerar en el disponible los créditos para operar asignados en Back Office.
        :param fecha_colocacion_hasta: Se usa en licitaciones, es la fecha de liquidación del proceso de licitación.
        :param es_bloqueado_bcra: Indica si se discriminan los USD que no se pueden utilizar para compras según BCRA 7340
        """
        req_body = {
          "cuenta": cuenta,
          "fechaDisponible": fecha_disponible.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "moneda": moneda,
          "diasRescatesPendientes": dias_rescates_pendientes,
          "diasSuscripcionesPendientes": dias_suscripciones_pendientes,
          "plazo": plazo,
          "incluyeCreditos": incluye_creditos,
          "fechaColocacionHasta": fecha_colocacion_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "esBloqueadoBcra": es_bloqueado_bcra
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-disponible-mon",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_tenencia_val(
            self,
            cuenta: str,
            fecha: datetime = datetime.now(),
            por_concertacion: bool = True,
            es_consolidado: bool = False,
            agrupar_por_moneda: bool = True,
            moneda_valuacion: str = "ARS",
            incluir_ppp: bool = False,
            incluir_monedas: bool = True,
            incluir_titulos: bool = False,
            incluir_opciones: bool = False,
            incluir_futuros: bool = False,
            incluir_fondos: bool = False,
            valuar_posicion: bool = True,
            utiliza_cotizaciones_online: bool = True
    ):
        """
        Esta consulta devuelve la tenencia valorizada de una cuenta a una determinada fecha.
        :param cuenta: Código de Comitente
        :param fecha: Fecha a la que se consultan las tenencias
        :param por_concertacion: Indica si las tenencias se buscan por Fecha de Concertación o no.
        :param es_consolidado: Indica si se muestran todas las cuentas del usuario consolidadas o solo la cuenta seleccionada.
        :param agrupar_por_moneda: Indica si agrupa los instrumentos por moneda de emisión.
        :param moneda_valuacion: Indica la moneda que se utiliza para valuar todos los instrumentos.
        :param incluir_ppp: Indica si se incluye PPP
        :param incluir_monedas: Indica si se incluyen tenencias de Monedas
        :param incluir_titulos: Indica si se incluyen tenencias de Titulos
        :param incluir_opciones: Indica si se incluyen tenencias de Opciones
        :param incluir_futuros: Indica si se incluyen tenencias de Futuros
        :param incluir_fondos: Indica si se incluyen tenencias de Fondos
        :param valuar_posicion: Indica si se debe valuar la posición o no
        :param utiliza_cotizaciones_online: Indica si utiliza cotizaciones online o busca directamente cotizaciones de VBolsa
        """
        req_body = {
            "cuentas": cuenta,
            "fecha": fecha.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "porConcertacion": por_concertacion,
            "esConsolidado": es_consolidado,
            "agruparPorMoneda": agrupar_por_moneda,
            "monedaValuacion": moneda_valuacion,
            "incluirPPP": incluir_ppp,
            "incluirMonedas": incluir_monedas,
            "incluirTitulos": incluir_titulos,
            "incluirOpciones": incluir_opciones,
            "incluirFuturos": incluir_futuros,
            "incluirFondos": incluir_fondos,
            "valuarPosicion": valuar_posicion,
            "utilizaCotizacionesOnLine": utiliza_cotizaciones_online
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-tenenciaval",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_tenencia_val_vencimientos(
            self,
            cuenta: str,
            fecha: datetime = datetime.now(),
            incluir_ppp: bool = True
    ):
        """
        Esta consulta devuelve la valuación de una cuenta a una determinada fecha (por liquidación) y los
        vencimientos posteriores a esa fecha.
        :param cuenta: Código de Comitente
        :param fecha: Fecha a la que se deben recuperar los movimientos que conforman los saldos. En esta consulta los movimientos se recuperan siempre por fecha de liquidación.
        :param incluir_ppp: Indica si se incluye ppp en la consulta. PPP se genera en un proceso de Vbolsa.
        """
        req_body = {
          "cuentas": cuenta,
          "fecha": fecha.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "incluirPPP": incluir_ppp
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-tenenciaval-vencimientos",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_rendimiento_cartera(
            self,
            cuenta: str,
            fecha_desde: datetime = datetime.now() - timedelta(days=15),
            fecha_hasta: datetime = datetime.now(),
            por_concertacion: bool = True
    ):
        """

        :param cuenta: Número de Cuenta Comitente
        :param fecha_desde: Fecha inicial del período de Rendimientos consultado.
        :param fecha_hasta: Fecha final del período de Rendimientos consultado.
        :param por_concertacion: Indica si saldos y movimientos involucrados en esta consulta se buscan por Fecha de Concertación o Liquidación.
        """
        req_body = {
          "cuenta": cuenta,
          "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
          "porConcertacion": por_concertacion
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-rendimiento-cartera",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_instrumentos(
            self,
            cod_tp_especie: int,
            page_number: int = 1,
            page_size: int = 200,
            solo_byma: bool = True
    ):
        """
        Es una consulta de Instrumentos que se pueden operar. Se toman de la tabla que registra todos los
        instrumentos para operar WEB. La respuesta es paginada.
        :param cod_tp_especie: Codigo interno del tipo de especie.
        :param page_number: Número de página a mostrar.
        :param page_size: Cantidad de registros por página.
        :param solo_byma:Indica si solo se recuperan los Instrumentos con Abreviaturas Byma. Por defecto informa solo Byma.
        """
        req_body = {
          "codTpEspecie": cod_tp_especie,
          "soloByMA": solo_byma,
          "paramPagination": {
            "pageNumber": page_number,
            "pageSize": page_size
          }
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-instrumentos-paginada",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_cotizaciones(self, instrumento: str, exact_match: bool = True):
        """
        Es una consulta de cotizaciones de instrumentos, se busca en la información en la tabla de cotizaciones
        online que registra cotizaciones para un mismo instrumento en distintas monedas y plazos
        :param instrumento: Abreviatura o descripción del instrumento. Se puede ingresar total o parcial dependiendo del siguiente parámetro.
        :param exact_match: Este parámetro indica si se debe busca exacto el texto ingresado o no.
        """
        req_body = {
          "instrumento": instrumento,
          "exactMatch": exact_match
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-cotizaciones",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_cotizaciones_fondos(self):
        """
        Es una consulta de cotizaciones y datos de Fondos Comunes de Inversión. Se informan las cotizaciones
        cargadas en VBolsa.
        :return:
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-cotizaciones-fondos",
            request_body={},
            request_method=HTTPMethod.POST
        )

    def get_cotizaciones_historicas(
            self,
            instrumento: str,
            fecha_desde: datetime = datetime.now() - timedelta(days=7),
            fecha_hasta: datetime = datetime.now()
    ):
        """
        Es una consulta de cotizaciones históricas de un instrumento. Se informan las cotizaciones cargadas en VBolsa.
        :param instrumento: Abreviatura del instrumento, se puede ingresar cualquier abreviatura vinculada. Se recupera la cotización de cierre que está cargada en VBolsa, la abreviatura se usa para ubicar el instrumento.
        :param fecha_desde: Fecha inicial de la consulta.
        :param fecha_hasta: Fecha final de la consulta.
        """
        req_body = {
            "instrumento": instrumento,
            "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-cotizaciones-historicas",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_cotizaciones_historicas_fci(
            self,
            instrumento: str,
            fecha_desde: datetime = datetime.now() - timedelta(days=7),
            fecha_hasta: datetime = datetime.now()
    ):
        """
        Es una consulta de cotizaciones históricas de un FCI. Se informan las cotizaciones cargadas en VBolsa.
        :param instrumento: Código de Interfaz Bloomberg del Fondo.
        :param fecha_desde: Fecha inicial de la consulta.
        :param fecha_hasta: Fecha final de la consulta.
        """
        req_body = {
            "instrumento": instrumento,
            "fechaDesde": fecha_desde.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            "fechaHasta": fecha_hasta.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-cotizaciones-historicas-fci",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_instrumento(self, abreviatura: str):
        """
        Devuelve los instrumentos filtrados por su abreviatura.
        :param abreviatura: Abreviatura del instrumento, se puede ingresar cualquier abreviatura vinculada.
        """
        req_body = {
          "abreviatura": abreviatura
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-instrumento",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_cotizaciones_cierre_search(self, instrumento: str, mercado: str = "ME"):
        """
        Es una consulta de cotizaciones de cierre de instrumentos
        :param instrumento: Abreviatura del instrumento, se puede ingresar cualquier abreviatura vinculada. Se recupera la cotización de cierre que esta cargada en VBolsa, la abreviatura se usa para ubicar el instrumento.
        :param mercado: Mercado al cual corresponde la abreviatura ingresada. Default: ME (ByMA)
        :return:
        """
        req_body = {
          "instrumento": instrumento,
          "mercado": mercado
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-cotizaciones-cierre-search",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_monedas(self):
        """
        Devuelve la lista de Monedas habilitadas.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-monedas",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_feriados(self):
        """
        Devuelve la lista de Feriados habilitados.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-feriados",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_provincias(self):
        """
        Devuelve la lista de Provincias habilitadas.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-provincias",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_paises(self):
        """
        Devuelve la lista de Paises habilitados.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-paises",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_tipos_especies(self):
        """
        Devuelve la lista de tipos de especies.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-tipos-especies",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_tipos_fondos(self):
        """
        Devuelve la lista de tipos de especies.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-tipos-fondos",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_tipos_riesgo_comitente(self):
        """
        Devuelve la lista de tipos de riesgo de Comitente.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-tipos-riesgo-comitente",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_detalle_cuenta(self, cuenta: str):
        """
        Esta consulta muestra el detalle de datos de la cuenta
        :param cuenta: Número de Comitente.
        """
        req_body = {
            "cuenta": cuenta,
            "timeStamp": 13128022,
            "paramPagination": {
                "pageNumber": 1,
                "pageSize": 1
            }
        }
        self.__pre_connection()
        return self.__make_request(
            request_endpoint="/get-detalle-cuenta",
            request_body=req_body,
            request_method=HTTPMethod.POST
        )

    def get_cuentas_por_cuit(self, cuit: str):
        """
        Es una consulta que informa las cuentas comitente que corresponden al CUIT ingresado. El cuit puede
        ser del comitente o de los condóminos.
        :param cuit: Nro de CUIT a buscar. Se deben ingresar solo numeros.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-cuentas-por-cuit?CUIT={cuit}",
            request_body={},
            request_method=HTTPMethod.GET
        )

    def get_persona(self, num_doc: int, tipo_doc: int = 1):
        """
        Retorna datos de una persona filtrando por tipo y número de documento.
        :param num_doc: Número de documento de la Persona a buscar.
        :param tipo_doc: Código del Tipo de Documento. 1: DNI, 2: Pasaporte, 3: Otros.
        """
        self.__pre_connection()
        return self.__make_request(
            request_endpoint=f"/get-persona?tipoDoc={tipo_doc}&numDoc={num_doc}",
            request_body={},
            request_method=HTTPMethod.GET
        )
