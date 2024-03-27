import fs from 'fs';
import path from 'path';
import {S3Client, PutObjectCommand} from '@aws-sdk/client-s3';

const s3Client = new S3Client({});

const uploadToS3 = async (bucket: string | undefined, key: string, file: string | Buffer) => {
	const fileContent = file instanceof Buffer ? file : fs.readFileSync(file);

	const command = new PutObjectCommand({
		Bucket: bucket,
		Key: key,
		Body: fileContent,
	});
	await s3Client.send(command);
};

const addPrefixToS3Path = (prefix: string, filePath: string) => path.join(prefix, filePath);

export {
	s3Client, uploadToS3, addPrefixToS3Path,
};
