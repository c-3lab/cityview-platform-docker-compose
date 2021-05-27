# cityview-platform


# 概要

地域の課題やイベントなどの情報を地図上に可視化するプラットフォームです。

<img width="1000" alt="スクリーンショット 2021-05-20 18 57 23" src="https://user-images.githubusercontent.com/6661165/118959449-4b581580-b99d-11eb-9809-a8bc9366db39.png">


## 構成

本プラットフォームの構築にはFIWARE(IoTプラットフォーム)を活用しております。  
簡易的にFIWAREのコンポーネントを立ち上げて体験できるようにdocker-composeで提供しております。

### FIWAREコンポーネント

* [Orion](https://github.com/telefonicaid/fiware-orion)
* [Cygnus](https://github.com/telefonicaid/fiware-cygnus)
* [WireCloud](https://github.com/Wirecloud/wirecloud)
* [Knowage](https://github.com/KnowageLabs/Knowage-Server)
* [Meteoroid](https://github.com/OkinawaOpenLaboratory/fiware-meteoroid)

# 起動方法

リポジトリのクローンをします。

```
git clone https://github.com/c-3lab/cityview-platform-docker-compose
cd cityview-platform-docker-compose
```

## FIWARE OrionとFIWARE Cygnusの起動

OrionとCygnusを起動します。

```
docker-compose up -d
```


## WireCloudの起動

WireCloudを起動します。  
※ WireCloudで使うDBは一つ前のdokcer-compose.yamlで立ち上げたPostgreSQLが流用されます。

```
docker-compose -f docker-compose-wirecloud.yaml up -d
```

WireCloud用のスーパーユーザを作成します。

```
docker-compose -f docker-compose-wirecloud.yaml exec wirecloud python manage.py createsuperuser
```

スーパーユーザの情報を対話形式で入力します。

```
Username (leave blank to use 'root'): ユーザ名
Email address: メールアドレス
Password: パスワード
Password (again): パスワード再入力
Superuser created successfully.
```


## Knowageの起動

Knowageを起動します

```
docker-compose -f docker-compose-knowage.yaml up -d
```


## Meteoroidの起動

Meteoroidの起動に必要となる[OpenWhisk](https://github.com/apache/openwhisk-devtools)を取得します

```
git clone https://github.com/apache/openwhisk-devtools.git
```

OpenWhiskを実行します

```
cd openwhisk-devtools/docker-compose/
make quick-start
```

Meteoroidを起動します

```
docker-compose -f docker-compose-meteoroid.yaml up -d
```

### Functionの作成

Meteoroidのcliツールをインストールします。(Python3.8以上が必要です)

```
pip install meteoroid-cli
```

MeteoroidのFunctionを作成します。

```
meteoroid function create import-csv meteoroid-function/main.py
```

**実行結果**  
次の手順のEndpoint作成でこのidを使用します。   
`meteoroid function list`コマンドでも確認できます。

```
+---------------------+---------------------------------------------------------------------+
| Field               | Value                                                               |
+---------------------+---------------------------------------------------------------------+
| id                  | 1                                                                   |
| code                | import csv                                                          |
|                     | from datetime import datetime                                       |
|                     | import dateutil.parser                                              |
|                     | import io                                                           |
|                     | import requests                                                     |
|                     | import uuid                                                         |
|                     |                                                                     |
|                     | ~~省略~~                                                             |
|                     | if __name__ == '__main__':                                          |
|                     |     main({'__ow_body': 'bear,beast,0,1,1753-01-01T00:00:00+09:00'}) |
|                     |                                                                     |
| language            | python:default                                                      |
| binary              | False                                                               |
| main                |                                                                     |
| version             | 0.0.1                                                               |
| parameters          | []                                                                  |
| fiware_service      |                                                                     |
| fiware_service_path | /                                                                   |
| name                | import-csv                                                          |
+---------------------+---------------------------------------------------------------------+

```

FunctionへアクセスできるようにMeteoroidのEndpointを作成します。  
先ほど作成したFunctionのidを最後に指定します。

```
meteoroid endpoint create nuisance_wildlife /import-csv post <作成したFunction id>
```

**実行結果**  
作成されたurlを確認します。

```
+---------------------+------------------------------------------------------------------------------------------------+
| Field               | Value                                                                                          |
+---------------------+------------------------------------------------------------------------------------------------+
| id                  | 1                                                                                              |
| url                 | http://192.168.11.4:9090/api/23bc46b1-71f6-4ed5-8c54-816aa4f8c502/nuisance_wildlife/import-csv |
| fiware_service      |                                                                                                |
| fiware_service_path | /                                                                                              |
| name                | nuisance_wildlife                                                                              |
| path                | /import-csv                                                                                    |
| method              | post                                                                                           |
| function            | 1                                                                                              |
+---------------------+------------------------------------------------------------------------------------------------+
```


### Functionの実行


先ほど作成したFunctionへサンプルデータの獣害情報を投入することでFIWARE Orionにデータが登録されます。  
指定するURLは先ほどEndpointで作成したURLを指定します。

```
curl -X POST <作成したEndpoint url> -H 'Content-Type: text/csv' --data-binary @meteoroid-function/sample.csv
```

**実行結果**  
以下の実行結果が出れば成功です。

```
HTTP/1.1 200 OK
Server: openresty
Date: Thu, 27 May 2021 00:59:58 GMT
Content-Type: application/json
Content-Length: 39
Connection: keep-alive
X-Request-ID: QXdvKLDgpaDausIXwAwYFbxjtvnIT8We
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
Access-Control-Allow-Headers: Authorization, Origin, X-Requested-With, Content-Type, Accept, User-Agent
x-openwhisk-activation-id: 8679b54d205d4377b9b54d205d037745
Access-Control-Allow-Credentials: true
X-Request-Id: QXdvKLDgpaDausIXwAwYFbxjtvnIT8We

{
  "count": 1,
  "status": "success"
}%
```

## WireCloudの設定

WireCloudを使って可視化用Web画面を構築していきます。  
ログイン画面にアクセスしてスーパーユーザでログインをします。(ユーザ名とパスワードは先ほどスーパーユーザの作成で設定した値)

[http://localhost:8000/login](http://localhost:8000/login)

<img width="600" alt="スクリーンショット 2021-05-26 22 04 33" src="https://user-images.githubusercontent.com/6661165/119664640-80b5a500-be6e-11eb-96a3-08ed2fe56bb9.png">


ハンバーガーメニューから「+ 新しいワークスペース」を選択します。

<img width="600" alt="スクリーンショット 2021-05-26 22 08 49" src="https://user-images.githubusercontent.com/6661165/119665142-0a657280-be6f-11eb-92b3-95419c3d2b32.png">


ワークスペース名を入力して作成します。

<img width="600" alt="スクリーンショット 2021-05-26 22 11 35" src="https://user-images.githubusercontent.com/6661165/119665428-57494900-be6f-11eb-9923-e96efd5ecd93.png">


### Widgetの追加

次にWidgetを追加します。    
WidgetはWireCloudにおいて画面を構成するために必要なコンポーネントとなっており、外部からダウンロードしたWidgetをWireCloudへアップロードすることで使うことができます。  
今回は以下のWidgetを使用します。 以下のダウンロードボタンを押して全てのWidgetをダウンロードします。 

* [ol3-map-widget](https://github.com/Wirecloud/ol3-map-widget)
  * [ダウンロード](https://github.com/Wirecloud/ol3-map-widget/releases/download/1.2.3/CoNWeT_ol3-map_1.2.3.wgt)
* [ngsi-source](https://github.com/wirecloud-fiware/ngsi-source)
  * [ダウンロード](https://github.com/wirecloud-fiware/ngsi-source-operator/releases/download/4.2.0/CoNWeT_ngsi-source_4.2.0.wgt)
* [ngsi-entity2poi-operator](https://github.com/wirecloud-fiware/ngsi-entity2poi-operator)
  * [ダウンロード](https://github.com/wirecloud-fiware/ngsi-entity2poi-operator/releases/download/v3.2.2/CoNWeT_ngsientity2poi_3.2.2.wgt)

マイ・リソースを押します。

<img width="300" alt="スクリーンショット 2021-05-26 22 16 16" src="https://user-images.githubusercontent.com/6661165/119666385-4b11bb80-be70-11eb-9858-442d7da89f67.png">

次にアップロードを押します。

<img width="300" alt="スクリーンショット 2021-05-26 22 19 18" src="https://user-images.githubusercontent.com/6661165/119666570-7399b580-be70-11eb-9543-009cc801d86e.png">

ダウンロードしたWidgetを画面にドラッグ&ドロップすることで追加することができます。ファイルの追加ができたらアップロードボタンを押します。

<img width="600" alt="スクリーンショット 2021-05-26 22 44 15" src="https://user-images.githubusercontent.com/6661165/119679715-8bc30200-be7b-11eb-9577-9b5fc3f09ae9.png">

### ワイヤリングで画面を作成

ペンマークを押すとワイヤリングなど画面の編集ができるようになります。

<img width="300" alt="スクリーンショット 2021-05-26 23 37 31" src="https://user-images.githubusercontent.com/6661165/119680223-f2e0b680-be7b-11eb-9d6c-34e57dfd77b7.png">

ワイヤリングを選択します。

<img width="300" alt="スクリーンショット 2021-05-26 23 37 37" src="https://user-images.githubusercontent.com/6661165/119680266-fbd18800-be7b-11eb-8518-0acf125a7575.png">

コンポーネントの検索を押します。

<img width="300" alt="スクリーンショット 2021-05-26 23 42 58" src="https://user-images.githubusercontent.com/6661165/119680458-2a4f6300-be7c-11eb-9154-a579a9e9bac0.png">

OpenLayers Mapの +ボタンを押すと下にオレンジのボックスが作成されます。そのボックスを右側の空白にドラッグ&ドロップします。

<img width="300" alt="スクリーンショット 2021-05-26 23 45 15" src="https://user-images.githubusercontent.com/6661165/119680792-75697600-be7c-11eb-9413-02aff2ad2abe.png">

青色のタブからオペレーター切り替えます。  
NGSI SourceとNGSI to PoIも同じように +ボタンを押し、作成された緑色の箱を右側の空白にドラッグ&ドロップします。

<img width="300" alt="スクリーンショット 2021-05-26 23 49 05" src="https://user-images.githubusercontent.com/6661165/119681374-f88acc00-be7c-11eb-8096-ed31d4c768df.png">

以下のようにWidgetの接続を行います。  
接続の方法は出っ張っている青色のコネクタを接続先のコネクタへドラッグ&ドロップします。

<img width="600" alt="スクリーンショット 2021-05-26 23 51 35" src="https://user-images.githubusercontent.com/6661165/119681772-51f2fb00-be7d-11eb-9614-b66292998c6c.png">

NGSI Sourceのハンバーガーメニューを押し、設定ボタンを押します。

<img width="600" alt="スクリーンショット 2021-05-27 0 43 44" src="https://user-images.githubusercontent.com/6661165/119690933-1825f280-be85-11eb-930f-07e07d3e3c82.png">

オペレータの設定を以下のように入力し設定を押します。

<img width="600" alt="スクリーンショット 2021-05-27 0 55 50" src="https://user-images.githubusercontent.com/6661165/119692396-566fe180-be86-11eb-894d-07fac7770ab4.png">


画面上部の戻るボタンを押します。

<img width="300" alt="スクリーンショット 2021-05-27 0 49 32" src="https://user-images.githubusercontent.com/6661165/119691328-73f07b80-be85-11eb-8f18-200d48aff0b2.png">

サンプルデータとして登録した情報が地図上にピンとして表示されています。ピンを押すと吹き出しが表示され詳細情報を見ることもできます。

<img width="600" alt="スクリーンショット 2021-05-27 10 09 59" src="https://user-images.githubusercontent.com/6661165/119750283-eee08300-bed3-11eb-8d1c-b9e575cda428.png">


---


# ライセンス

[MIT License](LICENSE)
