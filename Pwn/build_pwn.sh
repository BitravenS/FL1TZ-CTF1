echo "Beginning Pwn Build"
cd ./access*
sudo docker build -t access .
cd ../blind*
sudo docker build -t blind .
cd ../echo*2
sudo docker build -t echo2 .
cd ../echo*er
sudo docker build -t echo1 .
cd ../leak*
sudo docker build -t leak .
cd ../lib*
sudo docker build -t library .
cd ../sys*
sudo docker build -t syscal .
cd ../rev*
sudo docker build -t review .

echo "Done!"

