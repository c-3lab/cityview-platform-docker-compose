import csv
from datetime import datetime
import dateutil.parser
import io
import requests
import uuid

# データ投入先（FIWARE-Orion）
ORION_ENDPOINT: str = 'http://localhost:1026/v2'


def main(args):
    try:
        data: list = load_csv(args.get('__ow_body', ''))
        count: int = import_to_orion(data)
        return {
            'status': 'success',
            'count': count
        }
    except Exception as e:
        return {
            'status': 'error',
            "reason": '{0}'.format(e)
        }


def load_csv(text: str) -> list:
    """CSVデータ取込

    Args:
        text (str): CSV形式の文字列

    Returns:
        list: 取込後、変換した辞書のリスト
    """
    results: list = []
    reader = csv.reader(io.StringIO(text), skipinitialspace=True)
    for row in reader:
        data: dict = {
            'type': 'NuisanceWildlife',
            'id': 'NuisanceWildlife-{0}'.format(uuid.uuid4()),
            'animalName': row[0],
            'animalCategory': row[1],
            'location': {
                'latitude': float(row[2]),
                'longitude': float(row[3])
            },
            'time': dateutil.parser.isoparse(row[4])
        }

        results.append(data)

    return results


def import_to_orion(data: list) -> int:
    """orionにデータ取込を実行

    Args:
        data (list): 獣害データのリスト

    Returns:
        int: 取込件数
    """
    payload: dict = {
        'actionType': 'append',
        'entities': [convert_to_ngsi(x) for x in data]
    }
    url = ORION_ENDPOINT + '/op/update'
    response = requests.post(url, json=payload)
    # ステータスコードが200番台以外の場合は例外とする
    response.raise_for_status()

    return len(payload['entities'])


def convert_to_ngsi(data: dict) -> dict:
    """NGSIフォーマットに変換

    Args:
        data (dict): 獣害データ

    Returns:
        dict: 書式変換した辞書
    """
    latitude: float = data['location']['latitude']
    longitude: float = data['location']['longitude']

    payload: dict = {
        'id': data['id'],
        'type': data['type'],
        'animalName': {
            'type': 'Text',
            'value': data['animalName']
        },
        'animalCategory': {
            'type': 'Text',
            'value': data['animalCategory']
        },
        'location': {
            'type': 'geo:point',
            'value': f'{latitude}, {longitude}'
        },
        'time': {
            'type': 'DateTime',
            'value': data['time'].isoformat()
        }
    }

    return payload


if __name__ == '__main__':
    main({'__ow_body': 'bear,beast,0,1,1753-01-01T00:00:00+09:00'})
