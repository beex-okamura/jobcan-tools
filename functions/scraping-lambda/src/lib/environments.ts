const {
	DOWNLOAD_DIR: downloadDir,
	UPLOAD_BUCKET: uploadBucket,
} = process.env;

export const getEnvironments = () => ({
	downloadDir: downloadDir ?? '/tmp',
	uploadBucket,
});
