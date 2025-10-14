.PHONY: docker-build
docker-build:
	docker build -t music-recommendations .

.PHONY: docker-cli-file
docker-cli-file:
	docker run --rm \
	-v "./host-data:/app/data" \
	-v "./host-data/lastfm:/app/lastfm" \
	music-recommendations

.PHONY: docker-cli-interactive
docker-cli-interactive:
	docker run --rm -it \
	-v "./host-data:/app/data" \
	-v "./host-data/lastfm:/app/lastfm" \
	music-recommendations -i	

.PHONY: local-cli-file
local-cli-file:
	python3 musicrecs.py

.PHONY: local-cli-interactive
local-cli-interactive:
	python3 musicrecs.py -i
