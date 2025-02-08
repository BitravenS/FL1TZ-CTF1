echo "Beginning build"

cd Cap*
sudo docker compose build
sudo docker compose up -d

cd -
cd Warmup/warmup
sudo docker compose build
sudo docker compose up -d

cd -
cd 'blind leading the blind'/blinnosqli
sudo docker compose build
sudo docker compose up -d

cd -
cd interlinked/interlinked
sudo docker compose build
sudo docker compose up -d

cd -
cd juggle/'juggle (2)'/juggle
sudo docker compose build
sudo docker compose up -d
 
cd -
cd rebound/rebbound
sudo docker compose build
sudo docker compose up -d

cd -
cd sqli4ever/sqli4evr
sudo docker compose build
sudo docker compose up -d

cd -
cd xxx
sudo docker compose build
sudo docker compose up -d

echo "Done!"
