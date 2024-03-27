import { CommitmentPolicy, KmsKeyringNode, buildClient } from '@aws-crypto/client-node';

const {
    KMS_CUSTOMER_ALIAS_KEY_ARN,
    KMS_CUSTOMER_KEY_ARN = '',
} = process.env;

const { decrypt } = buildClient(CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT);
const keyring = new KmsKeyringNode({
	generatorKeyId: KMS_CUSTOMER_ALIAS_KEY_ARN,
	keyIds: [KMS_CUSTOMER_KEY_ARN]
})

export const decryptPassword = async (password: string) => {
    const { plaintext } = await decrypt(keyring, Buffer.from(password, 'base64'));
    return plaintext.toString();
}
