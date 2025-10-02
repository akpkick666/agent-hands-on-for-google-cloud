## エージェントシステムのデプロイ

## 前提条件
- ルートの [`README.md`](../../../../README.md) に記載のセットアップが完了していること
- Vertex AI User ロールが実行者に付与されていること
```bash
# IAM ロール付与
gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/aiplatform.user"
```

## マルチエージェントシステムのデプロイ

マルチエージェントシステムの詳細とローカル実行については、[`multi_agent/README.md`](../README.md) を参照してください。

### Cloud Run デプロイ

```bash
# IAM ロール付与
gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/run.sourceDeveloper"

gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/iam.serviceAccountUser"

# サービスアカウントに対する IAM ロール付与
gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role=roles/run.builder

# IAM ロール付与
gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/iam.serviceAccountCreator"

# Cloud Run 用のサービスアカウント作成
gcloud iam service-accounts create multi-agent-sa \
  --display-name="Service Account for multi-agent-service on Cloud Run"

# サービスアカウントに対する IAM ロール付与
gcloud projects add-iam-policy-binding "$GOOGLE_CLOUD_PROJECT" \
  --member="serviceAccount:multi-agent-sa@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"


# Cloud Run デプロイ
cd ~/agent-hands-on-for-google-cloud/server/agents/multi_agent/deploy

gcloud run deploy multi-agent-service-{YOUR_NAME} \
  --source . \
  --region "$REGION" \
  --project "$GOOGLE_CLOUD_PROJECT" \
  --no-allow-unauthenticated \
  --service-account "multi-agent-sa" \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION,GOOGLE_GENAI_USE_VERTEXAI=True"
```

([参考](https://cloud.google.com/run/docs/deploying-source-code?hl=ja))


### Cloud Run プロキシ実行

Cloud Run はアクセスに認証が必要な状態でデプロイされています（`--no-allow-unauthenticated`）。そのため、ブラウザから直接アクセスすることはできません。

アクセス方法として、**Cloud Run プロキシ**を使用する方法があります。Cloud Run を呼び出す IAM ロール「**Cloud Run サービス起動元（roles/run.servicesInvoker）**」がアクセスするユーザーに付与されている場合、Cloud Run プロキシを使用してローカル環境から呼び出すことができます。

```bash
# IAM ロール付与
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/run.servicesInvoker"

# プロキシ実行
gcloud run services proxy {SERVICE_NAME} \
  --project "$GOOGLE_CLOUD_PROJECT" \
  --region $REGION
```

上記コマンドを実行すると、ローカルの `http://localhost:8080` から認証済みで Cloud Run サービスにアクセスできるようになります。（[参考](https://cloud.google.com/run/docs/triggering/https-request?hl=ja#private)）


### Identity-Aware Proxy (IAP) の設定

Cloud Run サービスに対して、より高度な認証・認可を行いたい場合は、**Identity-Aware Proxy (IAP)** を使用できます。IAP を使用することで、アクセスを IAP を利用できる IAM ロール「**IAP で保護されたウェブアプリ ユーザー（roles/iap.httpsResourceAccessor）**」がアタッチされた Google アカウントやグループに制限することができます。

IAP は、以下 ２ パターンの構築方法があります。
1. ロードバランサに対して構成する
2. **Cloud Run サービスに直接構成する** ※今回はこちら

IAP では認証の対象として「**内部**」と「**外部**」を選択できます。
- 内部の場合、Google Cloud 組織内の Google Workspace ユーザーのみがアクセス可能となります。
- 外部の場合、アクセスを許可した任意のユーザーのみがアクセス可能となります。<br>
※**「Cloud Run サービスに直接構成する」方法では使用できません**

（[参考1](https://cloud.google.com/iap/docs/enabling-cloud-run?hl=ja)）
（[参考2](https://cloud.google.com/run/docs/securing/identity-aware-proxy-cloud-run?hl=ja)）


```bash
# サービスエージェント(IAP用のサービスアカウント)作成
gcloud beta services identity create --service=iap.googleapis.com --project=$GOOGLE_CLOUD_PROJECT

# IAM ロール付与
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member="user:$(gcloud config get-value account)" \
  --role="roles/iap.httpsResourceAccessor"

gcloud run services add-iam-policy-binding {SERVICE_NAME} \
--member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-iap.iam.gserviceaccount.com"  \
--role="roles/run.invoker" \
--region="$REGION"


# IAP 有効化
gcloud beta run services update {SERVICE_NAME} \
--region=$REGION \
--iap
```


組織内のアカウントで Cloud Run の URL にアクセスします。
Google の認可フローを完了するとアプリケーションにアクセスできます。



### ロールの整理
上位ロールに内包されている、または用途が重複している IAM ロールは削除しましょう。
