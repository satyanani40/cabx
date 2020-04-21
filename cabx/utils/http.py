from collections import namedtuple

HttpResponse = namedtuple("HttpError", ("code", "status", "message"))

SUCCESS = HttpResponse(200, "OK", "Request Succeeded")
BAD_REQUEST = HttpResponse(400, "bad_input", "")
UNPROCESSABLE_REQUEST = HttpResponse(422, "Unprocessable Entity", "")
UNKNOWN_SERVICE = HttpResponse(404, "unknown_resources", "Resource doesn't exist: {}")
SERVICE_UNAVAILABLE = HttpResponse(503,
                                   "service_unavailable",
                                   "Backend service unreachable: {}")
INTERNAL_SERVER_ERROR = HttpResponse(500,"Internal Server Error","")
UNAUTHORIZED  = HttpResponse(401,"Unauthorized ","")
