# 一条命令发布到 GitHub Pages
#
# 用法（只需一次登录）：
#   1)  gh auth login          # 选 GitHub.com -> HTTPS -> 浏览器登录
#   2)  .\publish.ps1          # 建仓库、推代码、开 Pages、打印可点链接
#
# 可选：.\publish.ps1 -Repo my-game -Private

param(
  [string]$Repo = "elite-campus",
  [switch]$Private
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Need($cmd) { if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) { throw "找不到 $cmd" } }
Need git
Need gh

gh auth status *> $null
if ($LASTEXITCODE -ne 0) { throw "还没登录 GitHub：先运行  gh auth login" }

$owner = gh api user -q .login
if (-not $owner) { throw "读取 GitHub 用户名失败" }
Write-Host "GitHub 用户：$owner" -ForegroundColor Cyan

if (-not (Test-Path .git)) { git init -b main | Out-Null }
git add -A
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
  git -c user.name="$owner" -c user.email="$owner@users.noreply.github.com" `
      commit -m "校园打：按 B 站视频改编的网页游戏" | Out-Null
}

$vis = if ($Private) { "--private" } else { "--public" }
git remote get-url origin *> $null
if ($LASTEXITCODE -ne 0) {
  gh repo create $Repo $vis --source . --remote origin --push
} else {
  git push -u origin main
}

# 开启 Pages（main 分支根目录）
$json = '{"source":{"branch":"main","path":"/"}}'
try {
  $json | gh api --method POST "repos/$owner/$Repo/pages" --input - *> $null
} catch {
  $json | gh api --method PUT "repos/$owner/$Repo/pages" --input - *> $null
}

$url = "https://$owner.github.io/$Repo/"
Write-Host ""
Write-Host "已提交，Pages 通常 30~90 秒后生效：" -ForegroundColor Green
Write-Host "  $url" -ForegroundColor Yellow
Write-Host ""
Write-Host "把上面这条链接发给我，我来生成评论区用的二维码图。" -ForegroundColor Gray
