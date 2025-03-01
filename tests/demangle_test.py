"""Contains tests for demangle.py module."""

from emb_spy import demangle


def test_demangle() -> None:
    """Test demangle() function."""
    test_cases = [
        (
            "_ZN3act10motionMode4home14HomeSlowlyModeD2Ev",
            "act::motionMode::home::HomeSlowlyMode::~HomeSlowlyMode()",
        ),
        (
            "_ZN3act13driveableAxis12PhysicalAxis11setVelocityEx.constprop.0",
            "act::driveableAxis::PhysicalAxis::setVelocity(long long) [clone .constprop.0]",
        ),
        (
            "_ZN8platform8mainLoopILb1ELb1ENS_14MasterPlatformILj1ELj1ELj0EEEN14interprocessor23ZeroCopyTransferManagerILj1EEENS3_24SharedInterprocessorDataENS_L9emptyPollMUlvE_ES8_S8_S8_S8_EEvRT1_RT2_jPN3act11AxisManagerEPT3_PN10peripheral7storage26RealTimeTransactionManagerERKT4_RKT5_RKT6_RKT7_RKT8_.constprop.0",  # pylint: disable=line-too-long
            "void platform::mainLoop<true, true, platform::MasterPlatform<1u, 1u, 0u>, interprocessor::ZeroCopyTransferManager<1u>, interprocessor::SharedInterprocessorData, platform::emptyPoll::{lambda()#1}, platform::emptyPoll::{lambda()#1}, platform::emptyPoll::{lambda()#1}, platform::emptyPoll::{lambda()#1}, platform::emptyPoll::{lambda()#1}>(platform::MasterPlatform<1u, 1u, 0u>&, interprocessor::ZeroCopyTransferManager<1u>&, unsigned int, act::AxisManager*, interprocessor::SharedInterprocessorData*, peripheral::storage::RealTimeTransactionManager*, platform::emptyPoll::{lambda()#1} const&, platform::emptyPoll::{lambda()#1} const&, platform::emptyPoll::{lambda()#1} const&, platform::emptyPoll::{lambda()#1} const&, platform::emptyPoll::{lambda()#1} const&) [clone .constprop.0]",  # pylint: disable=line-too-long
        ),
    ]

    for i, test_case in enumerate(test_cases):
        got = demangle(test_case[0])
        expected = test_case[1]
        assert got == expected, f"{i}: Got '{got}'. Expected '{expected}'."
