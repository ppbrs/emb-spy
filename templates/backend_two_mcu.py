"""Backend usage example with two MCUs."""
import logging

from emb_spy import Backend


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    port = Backend.find_openocd_telnet_port()
    target0 = None
    target1 = "master.cpu0"
    with Backend(port=port, target_name=target0, logger_suffix="0") as backend0, \
            Backend(port=port, target_name=target1, logger_suffix="1") as backend1:
        logging.info("Running user requests.")
        target_0 = backend0.request(cmd="target current", timeout=0.5)
        target_1 = backend1.request(cmd="target current", timeout=0.5)
        print(f"{target_0=}, {target_1=}")
    print("\n\n")


if __name__ == "__main__":
    main()
