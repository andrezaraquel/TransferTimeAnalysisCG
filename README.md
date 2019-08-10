# Transfer Time Analysis in Campina Grande

Repositório scripts python: https://github.com/analytics-ufcg/people-paths/tree/master/python/scripts

### Passo a passo:

1) Rodar BULMA/BUSTE c/ dados de GPS e GTFS

2) Levantar o OTP numa máquina(Tutorial: https://docs.google.com/document/d/1aNDCTQR39KqB8Z_6V97sxKTwgpFfQocUsPcPVtS7u68/edit) usando o GTFS e um mapa de CG

3) Rodar as queries to OTP utilizando esse script: get_otp_itineraries_cg.py

4) Inferir viagens realizadas a partir das programadas utilizando esse script: vehicle-otp-od-builder_cg.py

Notebook com esse último passo para debug/teste:https://github.com/analytics-ufcg/people-paths/blob/master/python/notebooks/trips-destination-inference/otp-od-builder-test.ipynb

### Exemplo de comandos

- Levantar o serviço do OTP: 

docker run -e JAVA_MX=2G -v <path>/otp/otp-graphs/graphs/:/data/ -p 5601:8080 goabout/opentripplanner otp --build /data/cg/

- Gerar o grafo da cidade: 

sudo docker run -e JAVA_MX=2G -v <path>/otp/otp-graphs/graphs/:/data/ -p 5601:8080 goabout/opentripplanner otp --autoScan --graphs /data --port 8080 --analyst

- Recuperar os itinerários:

python get_otp_itineraries_cg.python 

- Casa os itinerários (saída anterior) com os dados de GPS:

python vehicle_otp_od_builder_cg.py data/output/2019_05_13_user_trips_otp_itineraries.csv data/input data/input data/output


### Levantando OTP numa máquina

Pull docker image from: https://hub.docker.com/r/goabout/opentripplanner/
Download and Unzip OTP graphs data into vm 
Any doubts, follow this tutorial: http://docs.opentripplanner.org/en/latest/Basic-Tutorial/
Build graphs with current OTP jar:
docker run -e JAVA_MX=2G -v <OTP-graphs-folderpath>:/data -p <OTP-chosen-PORT>:8080 goabout/opentripplanner otp --build /data/<city-data-folder>/ &
Run OTP docker:
docker run -e JAVA_MX=2G -v <OTP-graphs-folderpath>:/data -p <OTP-chosen-PORT>:8080 goabout/opentripplanner otp --autoScan --graphs /data --port 8080 --analyst &

Sample Commands:

Build Graph:
docker run -e JAVA_MX=2G -v /local/tarciso/otp/graphs/:/data/ -p 5601:8080 goabout/opentripplanner otp --build /data/ctba/

Run OTP with Graph:
docker run -e JAVA_MX=2G -v /local/tarciso/otp/graphs/:/data -p 5601:8080 goabout/opentripplanner otp --autoScan --graphs /data --port 8080 --analyst &

Sample API Calls:

150.165.85.4:10402/otp/routers/ctba/plan?fromPlace=-25.39211,-49.22613&toPlace=-25.45102,-49.28381&mode=TRANSIT,WALK&date=04/03/2017&time=16:20:00

http://150.165.85.4:10402/otp/routers/cg/plan?fromPlace=-7.2090842,-35.900876&toPlace=-7.2194726,-35.8774872&mode=TRANSIT,WALK&date=04/03/2017&time=16:20:00

localhost:5601/otp/routers/cg/plan?fromPlace=-7.287365,-35.894520&toPlace=-7.217147,-35.909744&mode=TRANSIT,WALK&date=14/05/2019&time=16:20:00

