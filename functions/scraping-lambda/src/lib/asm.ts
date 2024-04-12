import { GetSecretValueCommand, SecretsManagerClient } from '@aws-sdk/client-secrets-manager';
import { SecretsValues } from '../entities/asm.ts';

const { SECRETS_KEY_NAME } = process.env

const ssm = new SecretsManagerClient({})

export const getSecretsValues = async (): Promise<SecretsValues> => {
    const results = await ssm.send(new GetSecretValueCommand({
        SecretId: SECRETS_KEY_NAME
    }));

    if (results.SecretString == undefined) return {} as SecretsValues;
    return JSON.parse(results.SecretString)
}
