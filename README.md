# Althea monitoring



# Installation

1. Install telegraf

```
sudo su

cat <<EOF | sudo tee /etc/apt/sources.list.d/influxdata.list
deb https://repos.influxdata.com/ubuntu bionic stable
EOF

sudo curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -

sudo apt-get update
sudo apt-get -y install telegraf jq bc

sudo systemctl enable --now telegraf
sudo systemctl is-enabled telegraf
systemctl status telegraf

# make the telegraf user
sudo adduser telegraf sudo
sudo adduser telegraf adm
sudo -- bash -c 'echo "telegraf ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers'

```

 2. Install influxdb
 
 ```
sudo su

# now install InfluxDB
apt-get install influxdb -y

# start InfluxDB and enable at start
systemctl enable --now influxdb
systemctl start influxdb

# Configure InfluxDB

# don't forget to change your password
influx
> create database telegraf
> use telegraf
> create user telegraf with password yourpassword
# or add '' #
> create user telegraf with password 'yourpassword'
> grant all on telegraf to telegraf

```

 3. Install Grafana
 
 ```
sudo su

wget -q -O - https://packages.grafana.com/gpg.key | apt-key add -

add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"

apt-get update -y
apt-get install grafana -y

systemctl daemon-reload

systemctl enable --now grafana-server
systemctl start grafana-server

systemctl status grafana-server



```

4. Configure telegraf

 ```
sudo su

cd ~
git clone https://github.com/yamat3h/altheamonitoring
cd altheamonitoring
chmod +x monitor.sh
sed -i -e 's/\r$//' monitor.sh
sudo rm -rf /etc/telegraf/telegraf.conf

# if you changed the password for Influxdb then change it in the config file telegraf.conf
cp telegraf.conf /etc/telegraf/telegraf.conf
systemctl restart telegraf

```
# Configure Grafana

 ```
# Don't forget to change your password
grafana-cli admin reset-admin-password yourpassword

# or add '' #

grafana-cli admin reset-admin-password 'yourpassword'

```
Open firewall 3000 port

go http://youip:3000

login: admin
pass: yourpassword

![Data](https://i.imgur.com/qlWDM94.png)

Then we press the button "Add data source"
then choose Influxdb

![Data](https://i.imgur.com/iVNDy2n.png)

fill in the values
Name: telegraf
URL: http://localhost:8086
Database: telegraf
User: telegraf
Password: yourpassword
(the one that you installed for influxdb)

Then we press the button "Save & Test"

![Data](https://i.imgur.com/6DdkSIA.png)

Then select import

![Import](https://i.imgur.com/fBiKWAF.png)

Then we press the button "Upload JSON file"

![Import](https://i.imgur.com/aHAdpGA.png)

Download the file "Althea Validator Dashboard.json" from the repository and indicate the path to it, then confirm the import, and now you have your own monitoring board!

![Finish](https://i.imgur.com/sEFFavv.png)
