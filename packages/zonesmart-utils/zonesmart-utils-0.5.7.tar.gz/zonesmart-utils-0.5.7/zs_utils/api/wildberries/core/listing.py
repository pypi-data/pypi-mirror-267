from zs_utils.api.wildberries.base_api import WildberriesAPI


class GetWildberriesNomenclatureList(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Kontent-Prosmotr/paths/~1content~1v1~1cards~1cursor~1list/post
    """

    http_method = "POST"
    resource_method = "content/v1/cards/cursor/list"
    required_params = ["sort"]


class GetWildberriesNomenclatureByVendorCode(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Kontent-Prosmotr/paths/~1content~1v1~1cards~1filter/post
    """

    http_method = "POST"
    resource_method = "content/v1/cards/filter"
    required_params = ["vendorCodes"]


class GetWildberriesPrices(WildberriesAPI):
    """
    https://openapi.wb.ru/prices/api/ru/#tag/Spiski-tovarov/paths/~1api~1v2~1list~1goods~1filter/get
    """

    http_method = "GET"
    resource_method = "api/v2/list/goods/filter"
    required_params = ["limit"]
    allowed_params = ["offset", "filterNmID"]


class UpdateWildberriesPrices(WildberriesAPI):
    """
    https://openapi.wb.ru/prices/api/ru/#tag/Ustanovka-cen-i-skidok/paths/~1api~1v2~1upload~1task/post
    """

    http_method = "POST"
    resource_method = "api/v2/upload/task"
    required_params = ["data"]


class CreateWildberriesBarcodes(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Kontent-Prosmotr/paths/~1content~1v1~1barcodes/post
    """

    http_method = "POST"
    resource_method = "content/v1/barcodes"
    required_params = ["count"]


class GetWildberriesFailedToUploadNomenclatureList(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Kontent-Prosmotr/paths/~1content~1v1~1cards~1error~1list/get
    """

    http_method = "GET"
    resource_method = "content/v1/cards/error/list"


class CreateWildberriesNomenclature(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Kontent-Zagruzka/paths/~1content~1v1~1cards~1upload/post
    """

    http_method = "POST"
    resource_method = "content/v1/cards/upload"
    array_payload = True


class UpdateWildberriesNomenclature(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Kontent-Zagruzka/paths/~1content~1v1~1cards~1update/post
    """

    http_method = "POST"
    resource_method = "content/v1/cards/update"
    array_payload = True


class AddWildberriesNomenclaturesToCard(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Kontent-Zagruzka/paths/~1content~1v1~1cards~1upload~1add/post
    """

    http_method = "POST"
    resource_method = "content/v1/cards/upload/add"
    required_params = [
        "vendorCode",
        "cards",
    ]


class UpdateWildberriesNomenclatureImages(WildberriesAPI):
    """
    https://openapi.wb.ru/#tag/Kontent-Mediafajly/paths/~1content~1v1~1media~1save/post
    """

    http_method = "POST"
    resource_method = "content/v1/media/save"
    required_params = [
        "vendorCode",
        "data",
    ]
