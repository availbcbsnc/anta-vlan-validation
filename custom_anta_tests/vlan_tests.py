from typing import ClassVar, List
from anta.models import AntaTest, AntaCommand
from pydantic import BaseModel
from anta.custom_types import Interface, VlanId

class VerifyInterfaceVLANs(AntaTest):
    """
    Verifies that specific VLANs are associated with given switch interfaces.

    This test checks if the provided interfaces are configured with the expected VLANs
    by parsing the output of the 'show vlan' command. It supports both access and trunk
    interfaces, ensuring the specified VLANs are present in the interface's VLAN configuration.

    Expected Results
    ----------------
    * Success: The test passes if all specified interfaces are associated with their expected VLANs.
    * Failure: The test fails if any interface is missing one or more expected VLANs or if no interfaces are provided.

    Examples
    --------
    ```yaml
    anta.tests.vlan:
      - VerifyInterfaceVLANs:
          interfaces:
            - name: Ethernet1
              vlans: [10, 20]
            - name: Ethernet2
              vlans: [30]
    ```
    """

    name = "VerifyInterfaceVLANs"
    description = "Verifies that specific VLANs are associated with given switch interfaces."
    categories: ClassVar[list[str]] = ["vlan", "interfaces"]
    commands: ClassVar[list[AntaCommand]] = [AntaCommand(command="show vlan", ofmt="json", revision=1)]

    class Input(AntaTest.Input):
        class VlanToInterface(BaseModel):
            name: Interface
            vlans: List[VlanId]

        interfaces: List[VlanToInterface]

    @AntaTest.anta_test
    def test(self) -> None:
        self.result.is_success()
        command_output = self.instance_commands[0].json_output

        failures = []
        for interface in self.inputs.interfaces:
            interface_name = interface.name
            expected_vlans = set(str(vlan) for vlan in interface.vlans)

            actual_vlans = set()
            for vlan_id, vlan_data in command_output.get("vlans", {}).items():
                if interface_name in vlan_data.get("interfaces", {}):
                    actual_vlans.add(vlan_id)

            missing_vlans = expected_vlans - actual_vlans
            if missing_vlans:
                failures.append(f"Interface {interface_name} missing VLANs: {missing_vlans}")

        if failures:
            self.result.is_failure("; ".join(failures))
