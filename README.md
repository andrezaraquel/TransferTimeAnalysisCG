# Transfer Time Analysis in Campina Grande

Repositório scripts python: https://github.com/analytics-ufcg/people-paths/tree/master/python/scripts

### Passo a passo:

Rodar BULMA c/ dados de GPS e GTFS
Rodar BUSTE c/ BULMA e GTFS

Gerar dados de bilhetagem no formato de entrada do OTP com base em origens/destinos desejados

Usar dados de bilhetagem gerados para obter viagens programadas utilizando o OTP

Levantar o OTP numa máquina(Tutorial: https://docs.google.com/document/d/1aNDCTQR39KqB8Z_6V97sxKTwgpFfQocUsPcPVtS7u68/edit) usando o GTFS e um mapa de CG

Rodar as queries to OTP utilizando esse script: https://github.com/analytics-ufcg/people-paths/blob/master/python/scripts/trips-destination-inference/get_otp_itineraries.py

Inferir viagens realizadas a partir das programadas utilizando esse script: https://github.com/analytics-ufcg/people-paths/blob/master/python/scripts/trips-destination-inference/vehicle-otp-od-builder.py

Notebook com esse último passo para debug/teste:https://github.com/analytics-ufcg/people-paths/blob/master/python/notebooks/trips-destination-inference/otp-od-builder-test.ipynb


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

