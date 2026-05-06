demo:
	python3 demo.py

verify-demo:
	python3 kernel/verify.py

export-aep:
	python3 examples/export_mvk_aep_bundle.py --bundle audit_bundle.json --out mvk-aep-bundle

verify-aep:
	python3 examples/export_mvk_aep_bundle.py --verify mvk-aep-bundle

run:
	python3 mvk.py --run

tamper:
	python3 mvk.py --tamper

replay:
	python3 mvk.py --replay
