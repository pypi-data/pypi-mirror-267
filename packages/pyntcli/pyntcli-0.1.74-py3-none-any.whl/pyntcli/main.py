from sys import argv, exit
import signal

import pyntcli.log.log as log
from pyntcli.commands import pynt_cmd
from pyntcli.pynt_docker import pynt_container
from pyntcli.ui import ui_thread
from pyntcli.ui import pynt_errors
from pyntcli.ui import ui_thread
from pyntcli.auth import login
from pyntcli.analytics import send as analytics
from requests.exceptions import SSLError
from pyntcli.transport.pynt_requests import InvalidPathException, InvalidCertFormat
from pyntcli.commands.util import HtmlReportNotCreatedException
from pyntcli.commands.util import SomeFoundingsOrWargningsException
from pyntcli.commands.postman import PyntWebSocketException
from pyntcli import __version__


def shutdown_cli():
    analytics.stop()
    pynt_container.PyntContainerRegistery.instance().stop_all_containers()
    ui_thread.stop()


def signal_handler(signal_number, frame):
    ui_thread.print(ui_thread.PrinterText("Exiting..."))

    shutdown_cli()

    exit(0)


def check_for_dependecies():
    pynt_container.get_docker_type()


def print_header():
    ui_thread.print(ui_thread.PrinterText(*ui_thread.pynt_header())
                             .with_line(*ui_thread.pynt_version())
                             .with_line(""))


def start_analytics():
    user_id = login.user_id()
    if user_id:
        analytics.set_user_id(user_id)
        log.add_user_details(user_id)


def main():
    print_header()
    try:
        log.set_source(__version__)
        start_analytics()
        check_for_dependecies()
        signal.signal(signal.SIGINT, signal_handler)
        cli = pynt_cmd.PyntCommand()
        cli.run_cmd(cli.parse_args(argv[1:]))
        analytics.stop()
    except pynt_cmd.PyntCommandException:
        pynt_cmd.root.usage()
    except pynt_container.DockerNotAvailableException:
        ui_thread.print(ui_thread.PrinterText("Docker was unavailable, please make sure docker is installed and running.", ui_thread.PrinterText.WARNING))
        analytics.emit(analytics.ERROR, {"error": "docker unavailable"})
    except SSLError:
        ui_thread.print(ui_thread.PrinterText("We encountered SSL issues and could not proceed, this may be the cause of a VPN or a Firewall in place. Run again with --insecure", ui_thread.PrinterText.WARNING))
    except login.Timeout:
        ui_thread.print(ui_thread.PrinterText("Pynt CLI exited due to incomplete registration, please try again.", ui_thread.PrinterText.WARNING))
        analytics.emit(analytics.ERROR, {"error": "login timeout"})
    except login.InvalidTokenInEnvVarsException:
        ui_thread.print(ui_thread.PrinterText("Pynt CLI exited due to malformed credentials provided in env vars.", ui_thread.PrinterText.WARNING))
        analytics.emit(analytics.ERROR, {"error": "invalid pynt cli credentials in env vars"})
    except pynt_container.ImageUnavailableException:
        analytics.emit(analytics.ERROR, {"error": "Couldn't pull pynt image and no local image found"})
        ui_thread.print(ui_thread.PrinterText("Error: Couldn't pull pynt image and no local image found.",ui_thread.PrinterText.WARNING))
    except HtmlReportNotCreatedException:
        analytics.emit(analytics.ERROR, {"error": "Html report was not created"})
        pynt_errors.unexpected_error()
    except InvalidPathException as e:
        ui_thread.print(ui_thread.PrinterText("Pynt CLI exited due to invalid host-CA path: {}".format(e), ui_thread.PrinterText.WARNING))
        analytics.emit(analytics.ERROR, {"error": "Host CA path provided was invalid"})
    except InvalidCertFormat as e:
        ui_thread.print(ui_thread.PrinterText("Pynt CLI exited due to invalid host-CA. Please provide a file in PEM format: {}".format(e), ui_thread.PrinterText.WARNING))
        analytics.emit(analytics.ERROR, {"error": "Host CA provided was not in valid pem format"})
    except PyntWebSocketException:
        analytics.emit(analytics.ERROR, {"error": "postman websocket failed to connect"})
        pynt_errors.unexpected_error()
    except SomeFoundingsOrWargningsException as e:
        exit(1)
    except Exception as e:
        analytics.emit(analytics.ERROR, {"error": "{}".format(e)})
        pynt_errors.unexpected_error()
    finally:
        log.flush_logger()
        shutdown_cli()


if __name__ == "__main__":
    main()
