push:
	@msg="$(filter-out $@,$(MAKECMDGOALS))"; \
	if [ -z "$$msg" ]; then \
		echo "Usage: make push \"commit message\""; \
		exit 1; \
	fi; \
	git add .; \
	git commit -m "$$msg"; \
	git push origin main

%:
	@:
