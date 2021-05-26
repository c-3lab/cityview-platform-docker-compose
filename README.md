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
WireCloudで使うDBは、一つ前のdokcer-compose.yamlで立ち上げたPostgreSQLを流用します。

```
docker-compose -f docker-compose-wirecloud.yaml up -d
```

WireCloud用のスーパーユーザを作成します。

```
docker-compose -f docker-compose-wirecloud.yaml exec wirecloud python manage.py createsuperuser
```


## Knowageの起動

Knowageを起動します

```
docker-compose -f docker-compose-knowage.yaml up -d
```


## Meteoroidの起動

Meteoroidの起動に必要となるOpenWhiskを取得します

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

---

# ライセンス

[MIT License](LICENSE)
