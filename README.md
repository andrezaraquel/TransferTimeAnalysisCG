#Transfer Time Analysis in Campina Grande

Repositório scripts python: https://github.com/analytics-ufcg/people-paths/tree/master/python/scripts

Passo a passo:

Rodar BULMA c/ dados de GPS e GTFS
Rodar BUSTE c/ BULMA e GTFS

Gerar dados de bilhetagem no formato de entrada do OTP com base em origens/destinos desejados

Usar dados de bilhetagem gerados para obter viagens programadas utilizando o OTP

Levantar o OTP numa máquina(Tutorial: https://docs.google.com/document/d/1aNDCTQR39KqB8Z_6V97sxKTwgpFfQocUsPcPVtS7u68/edit) usando o GTFS e um mapa de CG

Rodar as queries to OTP utilizando esse script: https://github.com/analytics-ufcg/people-paths/blob/master/python/scripts/trips-destination-inference/get_otp_itineraries.py

Inferir viagens realizadas a partir das programadas utilizando esse script: https://github.com/analytics-ufcg/people-paths/blob/master/python/scripts/trips-destination-inference/vehicle-otp-od-builder.py

Notebook com esse último passo para debug/teste:https://github.com/analytics-ufcg/people-paths/blob/master/python/notebooks/trips-destination-inference/otp-od-builder-test.ipynb

FIM
