import esbuild from 'esbuild'


esbuild.build({
  bundle: true, // バンドルするかどうか
  entryPoints: ['./src/handlers/handlers.ts', './src/execute.ts'],
  // entryPoints: ['./src/handlers/handler.ts'], // エントリーポイントのファイルパス
  outdir: './dict', // 出力先ディレクトリ
  platform: 'node', // 'node' 'browser' 'neutral' のいずれかを指定,
  format: 'esm',
  external: [], // バンドルに含めたくないライブラリがある場合は、パッケージ名を文字列で列挙する,
  banner: { // commonjs用ライブラリをESMプロジェクトでbundleする際に生じることのある問題への対策
    js: 'import { createRequire } from "module"; import url from "url"; const require = createRequire(import.meta.url); const __filename = url.fileURLToPath(import.meta.url); const __dirname = url.fileURLToPath(new URL(".", import.meta.url));',
  },
})