# HR Ad-Optimizer LP Implementation Plan

## Overview
求人原稿最適化プラットフォーム「HR Ad-Optimizer」のランディングページを **3パターン** 実装する。
各 .docx ファイルがそれぞれ独立したLP構成案であり、3つのHTMLを作成する。

- **Tech Stack**: HTML + CSS + JavaScript（フレームワークなし）
- **Design Concept**: 信頼感（青・紺）× 先進性（テック感）× 親しみやすさ（余白多め）- 共通デザインベース
- **Responsive**: モバイルファースト対応

## パターン対応表
| パターン | ソースドキュメント | 特徴 | ファイル名 |
|---------|-------------------|------|-----------|
| 1 | LP構成案.docx | コピーライティング特化・感情訴求型 | pattern1.html |
| 2 | 求人原稿最適化SaaS 開発要件 戦略定義書 ver3.0.docx | 機能・仕様特化・ロジカル訴求型 | pattern2.html |
| 3 | 求人原稿最適化プラットフォーム LP ワイヤーフレーム.docx | レイアウト特化・ビジュアル訴求型 | pattern3.html |

## Tasks

### Phase 1: 共通基盤（リセット＆再構築）
- [x] 1. 既存ファイルリセット・新ファイル構造作成 `cc:done`
- [x] 2. 共通CSS（変数・リセット・グリッド・ボタン・コンポーネント） `cc:done`
- [x] 3. 共通JS（スムーズスクロール・ハンバーガー・アニメーション） `cc:done`

### Phase 2: パターン1（LP構成案.docx ベース）
- [x] 4. P1: Header + ファーストビュー `cc:done`
- [x] 5. P1: 導入（The Reality）+ 解決策（The Solution） `cc:done`
- [x] 6. P1: 攻め（Attack）+ 守り（Defense）+ 進化（Evolution） `cc:done`
- [x] 7. P1: 開発者情報 + 利用シーン + クロージングCTA `cc:done`

### Phase 3: パターン2（戦略定義書 ベース）
- [x] 8. P2: Header + プロダクトコンセプト（FV） `cc:done`
- [x] 9. P2: ターゲット戦略 + Pain（課題） `cc:done`
- [x] 10. P2: システム仕様・処理モード + ハイブリッドエンジン `cc:done`
- [x] 11. P2: 承認UI + 学習機能 + ポジショニング + CTA `cc:done`

### Phase 4: パターン3（ワイヤーフレーム ベース）
- [x] 12. P3: Header + FV（2カラム: コピー + UIモックアップ） `cc:done`
- [x] 13. P3: 導入課題カード + 解決策ステップフロー `cc:done`
- [x] 14. P3: 機能詳細（タブ/セクション分割）+ 進化サイクル図 `cc:done`
- [x] 15. P3: 開発者プロフィール + 導入事例 + CTA `cc:done`

### Phase 5: 仕上げ
- [x] 16. 全パターン共通: スクロールアニメーション・レスポンシブ最終調整 `cc:done`
- [x] 17. パターン切替ナビ（index.html から3パターンへのリンク） `cc:done`
- [ ] 18. Codexレビュー + 指摘修正 `cc:TODO`
