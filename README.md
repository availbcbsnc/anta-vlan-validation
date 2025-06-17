# Custom ANTA Test: VerifyInterfaceVLANs

This repository demonstrates how to create and execute a **custom ANTA test** using the [Arista Network Test Automation (ANTA)](https://anta.arista.com) framework. The included test validates that specified VLANs are correctly configured on specified interfaces using EOS command output.

---

## 📁 Project Structure

```text
.
├── anta_inventory.yml               # Sample ANTA inventory file
├── custom_anta_tests/               # Python module for custom ANTA tests
│   ├── __init__.py
│   └── vlan_tests.py                # Custom test definition
├── custom_vlan_catalog.yml          # Test catalog referencing the custom test
├── pyproject.toml                   # Declares this as a Python project
└── requirements.txt                 # (Optional) dependencies for ANTA
```

---

## ✅ Test Overview: `VerifyInterfaceVLANs`

This test ensures that each interface defined in the input is configured with the specified VLANs. It uses the `show vlan` EOS command (JSON format) to determine actual interface memberships.

### ✔️ Pass Criteria
- Every specified interface must be associated with all listed VLANs.

### ❌ Fail Criteria
- Any VLAN missing from a specified interface results in failure. This includes partial matches.

### 🔧 Supported Interfaces
- Ethernet interfaces
- Port-Channels
- Any interface listed in `show vlan` output

---

## 🧪 Example Catalog Usage

```yaml
# custom_vlan_catalog.yml

custom_anta_tests.vlan_tests:
  - VerifyInterfaceVLANs:
      interfaces:
        - name: Ethernet1
          vlans: [10, 20]
        - name: Port-Channel1000
          vlans: [30]
```

---

## 🛠️ Setup Instructions

### 1. Install your custom test package
```bash
pip install -e .
```

### 2. Set your PYTHONPATH so ANTA can find your custom module
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/custom_anta_tests
```
Alternatively you can try this on windows after opening the current working directory in VS Code
```bash
$env:PYTHONPATH="$env:PYTHONPATH;$pwd"
```


### 3. Run the test
```bash
anta nrfu \
  -u <username> \
  -p <password> \
  --inventory anta_inventory.yml \
  --catalog custom_vlan_catalog.yml
```

---

## 🧩 Test Definition Summary

```python
class VerifyInterfaceVLANs(AntaTest):
    name = "VerifyInterfaceVLANs"
    description = "Verifies that specific VLANs are associated with given switch interfaces."
    categories = ["vlan", "interfaces"]
    commands = [AntaCommand(command="show vlan", ofmt="json", revision=1)]

    class Input(AntaTest.Input):
        class VlanToInterface(BaseModel):
            name: Interface
            vlans: List[VlanId]
        interfaces: List[VlanToInterface]
```

---

## 🔍 Output Example (Success)

```text
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Device  ┃ Test Name            ┃ Test Status ┃ Message(s) ┃ Test description                                      ┃ Test category    ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ A-LEAF1 │ VerifyInterfaceVLANs │ success     │            │ Verifies that specific VLANs are associated...        │ VLAN, Interfaces │
```

---

## 🔍 Output Example (Failure)

```text
╭────────────────────── Settings ──────────────────────╮
│ - ANTA Inventory contains 1 devices (AsyncEOSDevice) │
│ - Tests catalog contains 1 tests                     │
╰──────────────────────────────────────────────────────╯

[20:01:18] INFO     ANTA run starting ...                                                                                                                                                                                                                                                                    _runner.py:241
           INFO     ------- ANTA NRFU Run Information --------                                                                                                                                                                                                                                               _runner.py:455
                    Devices:                                                                                                                                                                                                                                                                                                
                      Total in initial inventory: 1                                                                                                                                                                                                                                                                        
                      Selected for testing: 1                                                                                                                                                                                                                                                                              
                    Total number of selected tests: 1                                                                                                                                                                                                                                                                      
                    ------------------------------------------                                                                                                                                                                                                                                                             
  • Running NRFU Tests...100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1/1 • 0:00:00 • 0:00:00

                                                                                         All tests results                                                                                         
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Device  ┃ Test Name            ┃ Test Status ┃ Message(s)                                        ┃ Test description                                                          ┃ Test category    ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ A-LEAF1 │ VerifyInterfaceVLANs │ failure     │ Interface Port-Channel1000 missing VLANs: {'100'} │ Verifies that specific VLANs are associated with given switch interfaces. │ VLAN, Interfaces │
└─────────┴──────────────────────┴─────────────┴───────────────────────────────────────────────────┴───────────────────────────────────────────────────────────────────────────┴──────────────────┘
```

---

## 📚 References
- [ANTA Custom Tests Documentation](https://anta.arista.com/stable/advanced_usages/custom-tests/)
- [ANTA CLI Documentation](https://anta.arista.com/stable/getting_started/cli/)
