"""Backend usage example with one MCU."""
import logging

from emb_spy import Backend


def main() -> None:
    """Connect to the default target and send a generic command."""
    logging.basicConfig(level=logging.INFO)
    with Backend(
        host="localhost",
        port=Backend.find_openocd_telnet_port(),
        target_name=None,
        logger_suffix=None,
        restart_if_not_running=True,
        halt_if_running=False,
    ) as backend:
        name, state = backend.get_current_target_state()
        print(f"State: {name=}, {state=}.")

        version = backend.request(cmd="version", timeout=0.5)
        print(version)

        target = backend.request(cmd="target current", timeout=0.5)
        print(target)

        # backend.request(cmd="reset", timeout=0.5)
    print("\n\n")


if __name__ == "__main__":
    main()
