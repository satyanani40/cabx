from collections import namedtuple

HttpResponse = namedtuple("HttpError", ("code", "status", "message"))

SUCCESS = HttpResponse(200, "OK", "Request Succeeded")
BAD_REQUEST = HttpResponse(400, "bad_input", "")
UNKNOWN_SERVICE = HttpResponse(404, "unknown_resources", "Resource doesn't exist: {}")
SERVICE_UNAVAILABLE = HttpResponse(503,
                                   "service_unavailable",
                                   "Backend service unreachable: {}")
