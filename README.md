### 技術要件

- Backend: Python3.12(pyenvとpoetry使用)
- API: FastAPI
- DB: sqlite3

### 内容

APIの部分のみの簡単なTODOアプリです

1. ユーザーはTODOリストを追加することができる。(認証機能は無し)
    1. TODOリストにはタイトルと締切、メモを追加することができる。
    2. TODOリストにはそれぞれ、子タスクを作成することができる。子タスクはその下に子タスクを持つことはできない。子タスクには、名前だけを持たせる。
2. タスクは古い順に上から並べて表示する。
3. ユーザーは上の検索ボタンからタスクの名前で検索を行うことができる。
4. TODOリストのデータはDBに保存されている。

参考にしたのはMicroSoftのTODOリストです。機能を絞ってありますが、もしも動作を確認したい場合は、以下のリンクからアクセスできます。

https://to-do.live.com/tasks

### 特徴

- リンターやフォーマッターを適切に設定
- リンターにはflake8、フォーマッターにはblackを使用
- TypeHintを記述
- ソースコードはGitで管理し、作成したソースコードはGitHubにアップロード

### 要件定義
1. **モデル定義**:
   - `Todo` モデル: タスクの情報を保持します。タイトル、締切、メモなどを持ちます。
   - `Step` モデル: 子タスクの情報を保持します。タイトルと親タスクのIDを持ちます。

2. **データベースの設定**:
   - SQLAlchemyを使用してデータベースを設定し、`Todo` と `Step` のテーブルを作成します。

3. **CRUD操作の実装**:
   - `crud.py` ファイルに、TODOリストと子タスクの作成、取得、更新、削除の関数を実装します。

4. **APIエンドポイントの作成**:
   - `/todos/`: GET、POSTエンドポイントを作成して、タスクの取得と作成を処理します。
   - `/todos/{todo_id}/steps/`: GET、POSTエンドポイントを作成して、指定したタスクの子タスクの取得と作成を処理します。

### ファイル構造
└── backend_todolist
    ├── __init__.py
    ├── crud.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── schemas.py

### 手順

最初にDocumentsにfastapi-appディレクトリを作って移動しておく

poetry init –name fast-api 等でpoetry環境を構築するとpyproject.tomlが生成される
この時に注意すべきがpythonのversionをしておかないと上手く回らない
今回はpython3.12.1で構築してるので

% poetry init --name backend_todolist
This command will guide you through creating your pyproject.toml config.
Version [0.1.0]:  3.12と設定する必要がある
Description []:  
Author:  
License []:  
Compatible Python versions [^3.12]: 

poetry shell で仮想環境を始めておき

poetry add xx で必要な物をダウンロードをする
fastapi
"uvicorn[standard]"
python-multipart jinja2
sqlalchemy

poetry add fastapi "uvicorn[standard]" python-multipart jinja2 sqlalchemy

app.py models.py database.py の中身を記述して

uvicorn app:app --reload とするとアプリがrunされる

https://dev.to/nditah/develop-a-simple-python-fastapi-todo-app-in-1-minute-8dg
このサイトの時はpython 3.10を使っていたのでimport impとなっていたが
今回はpython 3.12.1を使ったので impport importlibに直した

exitで仮想環境を終わらせる

poetry run pythonでファイルを実行する

環境変数 PYTHONPATH を設定して、モジュールのディレクトリをPythonに知らせることです。これは、コマンドラインで行うことができます。
export PYTHONPATH="/Users/aodori/Documents"
これを行わないとエラーが出る

### 各々のモジュールの作成順序とポイント
1.database.pyから作る
url
engine
session local 
base

2.model.pyでデータベースに送信する情報のclassを定義する
class:
idm title etc..

foreign keyとしてrelationship を追加する

3.schemas.pyにPydanticモデルを追加する
from pydantic import BaseModel
class:
id title str(型指定)
class
class(継承)etc..

4.crud.pyによく使うCRUD関数を格納しておく
In this file we will have reusable functions to interact with the data in the database.

Create a SQLAlchemy model instance with your data.
add that instance object to your database session.
commit the changes to the database (so that they are saved).
refresh your instance (so that it contains any new data from the database, like the generated ID).

def get_users(db: Session, skip: int = 0, limit: int = 100):
return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    	fake_hashed_password = user.password + "notreallyhashed"
    	db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    	db.add(db_user)
    	db.commit()
   	 db.refresh(db_user)

5. main.pyを書く
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

のように@appの様な関数を書いておき、実際データベースと更新する作業をさせる

uvicornによりサーバーを活性化させて確認する
