const { Octokit } = require("@octokit/core");
const sodium = require("libsodium-wrappers");

import * as config from "./config.json";

const pat = config.pat;
const owner = config.owner;
const repo = config.repo;

const octokit = new Octokit({
  auth: pat,
});

const getPublicKey = async () => {
  return await octokit.request(
    "GET /repos/{owner}/{repo}/actions/secrets/public-key",
    {
      owner: owner,
      repo: repo,
      headers: {
        "X-GitHub-Api-Version": "2022-11-28",
      },
    },
  );
};

const encrypt = async (key, secret) => {
  return new Promise((resolve) => {
    sodium.ready.then(() => {
      const binkey = sodium.from_base64(key, sodium.base64_variants.ORIGINAL);
      const binsec = sodium.from_string(secret);
      const encBytes = sodium.crypto_box_seal(binsec, binkey);
      const encryptedValue = sodium.to_base64(
        encBytes,
        sodium.base64_variants.ORIGINAL,
      );
      resolve(encryptedValue);
    });
  });
};

const createSecret = async (repoKey, secretName, secret) => {
  const encryptedValue = await encrypt(repoKey.data.key, secret);

  await octokit.request(
    "PUT /repos/{owner}/{repo}/actions/secrets/{secret_name}",
    {
      owner: owner,
      repo: repo,
      secret_name: secretName,
      encrypted_value: encryptedValue,
      key_id: repoKey.data.key_id,
      headers: {
        "X-GitHub-Api-Version": "2022-11-28",
      },
    },
  );
};

const createDependabotSecret = async (repoKey, secretName, secret) => {
  // await octokit.request('PUT /repositories/{repository_id}/environments/{environment_name}/secrets/{secret_name}', {
  //   repository_id: 'REPOSITORY_ID',
  //   environment_name: 'ENVIRONMENT_NAME',
  //   secret_name: 'SECRET_NAME',
  //   encrypted_value: 'c2VjcmV0',
  //   key_id: '012345678912345678',
  //   headers: {
  //     'X-GitHub-Api-Version': '2022-11-28'
  //   }
  // })
};

const createEnvSecret = async (repoKey, secretName, secret) => {
  // await octokit.request('PUT /repositories/{repository_id}/environments/{environment_name}/secrets/{secret_name}', {
  //   repository_id: 'REPOSITORY_ID',
  //   environment_name: 'ENVIRONMENT_NAME',
  //   secret_name: 'SECRET_NAME',
  //   encrypted_value: 'c2VjcmV0',
  //   key_id: '012345678912345678',
  //   headers: {
  //     'X-GitHub-Api-Version': '2022-11-28'
  //   }
  // })
};

const createRepoSecrets = async (repoKey) => {
  await createSecret(repoKey, "AWS_ACCOUNT_ID", config.aws_account_id);
  await createSecret(repoKey, "AWS_REGION", config.aws_region);
  await createSecret(repoKey, "RIOT_KEY", config.riot_key);
};

const createDependabotRepoSecrets = async (repoKey) => {};

const createEnvSecrets = async (repoKey) => {};

const run = async () => {
  const publicKey = await getPublicKey();

  await createRepoSecrets(publicKey);
  await createEnvSecrets(publicKey);
  await createDependabotRepoSecrets(publicKey);
};

run();
