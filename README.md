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

Meteoroidのcliツールをインストールします(Python3.8以上が必要です)

```
pip install meteoroid-cli
```

MeteoroidのFunctionを作成します

```
meteoroid function create import-csv meteoroid-function/main.py
```

FunctionへアクセスできるようにMeteoroidのEndpointを作成します

```
meteoroid endpoint create nuisance_wildlife /import-csv post <function_id>
```

### Functionの実行


先ほど作成したFunctionへサンプルデータの獣害情報を投入することでFIWARE Orionにデータが登録されます

```
curl -X POST https://localhost:9090/api/4be9b685-d926-499e-b6cd-52f16ff03089/nuisance_wildlife/import-csv -H 'Content-Type: text/csv' --data-binary @meteoroid-function/sample.csv
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


必要なWidgetをダウンロードします。  
WidgetはWireCloudで画面を構成するコンポーネントとなっており、ダウンロードしたWidgetをアップロードすることで使うことができます。  
今回は以下のWidgetを使用します。 以下のダウンロードボタンを押して全てのWidgetをダウンロードします。 

* [ol3-map-widget](https://github.com/Wirecloud/ol3-map-widget)
  * [ダウンロード](https://github.com/Wirecloud/ol3-map-widget/releases/download/1.2.3/CoNWeT_ol3-map_1.2.3.wgt)
* [ngsi-source](https://github.com/wirecloud-fiware/ngsi-source)
  * [ダウンロード](https://github.com/wirecloud-fiware/ngsi-source-operator/releases/download/4.2.0/CoNWeT_ngsi-source_4.2.0.wgt)
* [ngsi-entity2poi-operator](https://github.com/wirecloud-fiware/ngsi-entity2poi-operator)
  * [ダウンロード](https://github.com/wirecloud-fiware/ngsi-entity2poi-operator/releases/download/v3.2.2/CoNWeT_ngsientity2poi_3.2.2.wgt)

マイ・リソースを押します。

<img width="322" alt="スクリーンショット 2021-05-26 22 16 16" src="https://user-images.githubusercontent.com/6661165/119666385-4b11bb80-be70-11eb-9858-442d7da89f67.png">

次にアップロードを押します。

<img width="302" alt="スクリーンショット 2021-05-26 22 19 18" src="https://user-images.githubusercontent.com/6661165/119666570-7399b580-be70-11eb-9543-009cc801d86e.png">



---


# ライセンス

[MIT License](LICENSE)
