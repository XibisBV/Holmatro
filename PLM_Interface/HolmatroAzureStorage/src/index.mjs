const {
  TENANT_ID,
  CLIENT_ID,
  CLIENT_SECRET,
  ACCOUNT_NAME,
  BLOB_API_VERSION = "2023-11-03"
} = process.env;

async function getAccessToken() {
  const url = `https://login.microsoftonline.com/${TENANT_ID}/oauth2/v2.0/token`;
  const params = new URLSearchParams();
  params.append("grant_type", "client_credentials");
  params.append("client_id", CLIENT_ID);
  params.append("client_secret", CLIENT_SECRET);
  params.append("scope", "https://storage.azure.com/.default");

  const resp = await fetch(url, {
    method: "POST",
    body: params
  });

  if (!resp.ok) {
    throw new Error(`Token request failed: ${resp.status} ${await resp.text()}`);
  }

  const data = await resp.json();
  return data.access_token;
}

async function fetchBlob(container, blob, token) {
  const url = `https://${ACCOUNT_NAME}.blob.core.windows.net/${container}/${blob}`;
  const resp = await fetch(url, {
    headers: { Authorization: `Bearer ${token}`,
          "x-ms-version" : BLOB_API_VERSION,
          "x-ms-date" : new Date().toUTCString()
         }
  });

  const buf = Buffer.from(await resp.arrayBuffer());
  return {
    status: resp.status,
    contentType: resp.headers.get("content-type") || "application/octet-stream",
    body: buf
  };
}

export const handler = async (event) => {
  const container = event.pathParameters.container;
  const blob = event.pathParameters.blob;

  const token = await getAccessToken();
  const { status, contentType, body } = await fetchBlob(container, blob, token);

  return {
    statusCode: status,
    headers: { "Content-Type": contentType },
    isBase64Encoded: true,
    body: body.toString()
  };
};