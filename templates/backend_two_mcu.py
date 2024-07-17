"""Backend usage example with two MCUs."""
import logging

from emb_spy import Backend


def main() -> None:
    """Connect to two specific targets in one chain and send generic commands."""
    logging.basicConfig(level=logging.INFO)
    port = Backend.find_openocd_telnet_port()
    target0 = "master.cpu0"
    target1 = "axis1.cpu0"
    with Backend(port=port, target_name=target0, logger_suffix="0") as backend_0, \
            Backend(port=port, target_name=target1, logger_suffix="1") as backend_1:
        logging.info("Running user requests.")
        target_0 = backend_0.request(cmd="target current", timeout=0.5)
        target_1 = backend_1.request(cmd="target current", timeout=0.5)
        print(f"{target_0=}, {target_1=}")


if __name__ == "__main__":
    main()
