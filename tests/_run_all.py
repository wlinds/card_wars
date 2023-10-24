import importlib
import os
import subprocess
import sys
import time

files = os.listdir("tests")
current_script = os.path.basename(__file__)

files.remove(current_script)

found_modules = []
failed_modules = []
tests_count = 0
ran_tests = set()

for file in files:
    if file.endswith(".py") and file != "__init__.py":
        module_name = file[:-3]
        print(f"Found {module_name}")
        found_modules.append(module_name)
        time.sleep(0.025)

print(f"\nFound {len(found_modules)} modules...")
time.sleep(0.625)

output_file = "test_output.txt"
with open(output_file, "w") as f:
    for file in files:
        if file.endswith(".py") and file != "__init__.py":
            module_name = file[:-3]
            module = importlib.import_module(module_name)
            if "main" in dir(module):
                module.main()

            try:
                if hasattr(module, "unittest"):
                    f.flush()
                    subprocess.call([sys.executable, "-m", "unittest", module_name], stdout=f)
                    tests_count += 1
                    ran_tests.add(module_name)
                if hasattr(module, "card_build_test"):
                    module.card_build_test()
                    tests_count += 1
                    ran_tests.add(module_name)
                if hasattr(module, "goblin_vs_gnomes_test"):
                    module.goblin_vs_gnomes_test()
                    tests_count += 1
                    ran_tests.add(module_name)
                if hasattr(module, "test_all_minion"):
                    module.test_all_minion()
                    tests_count += 1
                    ran_tests.add(module_name)
                if hasattr(module, "taunt_test"):
                    module.taunt_test()
                    tests_count += 1
                    ran_tests.add(module_name)
            except Exception as e:
                print(f"Error in {module_name}: {e}")
                failed_modules.append(module_name)

print(f"\n{tests_count} tests successfully found and ran out of {len(found_modules)} modules.")

if failed_modules:
    print(f"The following modules did not run successfully: {', '.join(failed_modules)}")

not_tested_modules = set(found_modules) - ran_tests
if not_tested_modules:
    print(f"The following modules did not run any tests: {', '.join(not_tested_modules)}")

with open(output_file, "r") as f:
    print(f.read())

os.remove(output_file)
