# ealdoshkin.github.io

Личный сайт-блог [vyrn.ru](https://vyrn.ru): Hugo + тема [LoveIt](https://github.com/dillonzq/LoveIt) (вендорена в `themes/LoveIt`), деплой на GitHub Pages из ветки `prod`.

## Требования

- Hugo **0.165.0 extended** (`hugo version`)
- Node.js не нужен

## Разработка

```sh
hugo server -D          # http://localhost:1313, -D показывает черновики
hugo --gc --minify      # прод-сборка в public/
```

## Деплой

Пуш в `prod` → GitHub Actions собирает сайт и деплоит на Pages (`.github/workflows/hugo.yaml`). Домен `vyrn.ru` подключён через Settings → Pages, Enforce HTTPS включён.

## Структура контента

Посты — leaf bundles в `content/posts/<slug>/`:

```
content/posts/basic-golang/
├── index.en.md        # английская версия
├── index.ru.md        # русская версия
└── golang-basic.jpeg  # featured-изображение (исходник)
```

URL поста задаётся `[permalinks] posts = ":filename"` → `/basic-golang/`. Черновик — `draft: true` во front matter (не публикуется, но ресурсы сборятся).

## Изображения (Hugo Pipes)

Все картинки сайта проходят через override `layouts/partials/plugin/img.html`:

- **Исходники** лежат рядом со статьёй в page bundle (или в `static/`) — в git только они.
- **Производные** (webp-версии 480/800/1200/1600px, имена вида `имя_hu<hash>.webp`) генерируются при сборке в `public/` и в git не попадают; кэш обработки — `resources/_gen/`, тоже игнорируется.
- В HTML рендерится `srcset` с width-дескрипторами + `data-sizes="auto"` (lazysizes выбирает подходящий размер); фолбэк `src` — самый крупный webp.
- SVG и GIF не обрабатываются (вектор/анимация), картинки из `static/` не обрабатываются (нельзя резолвить из assets) — они идут как есть.
- `og:image` намеренно указывает на исходный jpeg — некоторые краулеры не понимают webp.
- width/height атрибуты проставляются автоматически (защита от layout shift).

**Как добавить картинку к посту:** положить файл в папку поста и указать во front matter:

```toml
resources:
  - name: "featured-image"
    src: "golang-basic.jpeg"
```

Больше ничего — размеры и форматы сборка сделает сама.

## Project-override-ы (поверх темы)

| Файл | Зачем |
|---|---|
| `layouts/partials/plugin/img.html` | Hugo Pipes: webp-srcset, width/height, alt из Title |
| `layouts/partials/head/link.html` | hreflang en/ru/x-default |
| `layouts/robots.txt` | свой robots.txt (Allow: /) |
| `layouts/_default/term.html` | рендер страниц тегов (в теме отсутствовал) |
| `layouts/shortcodes/{x,x_simple,instagram}.html` | замена удалённых internal-шорткодов Hugo (твит/инстаграм-встраивания) |
| `layouts/partials/internal/{x,x_simple}.html` | то же, для внутреннего шорткода |
| `i18n/ru.toml` | русский язык для виджетов (тема фолбэчится на en) |

Коммитить правки в `themes/LoveIt` избегаем — всё через override-ы; исключение (патчи темы) исторически минимально.

## Комментарии

[giscus](https://giscus.app) — комментарии через GitHub Discussions этого репозитория (категория *Announcements*). Конфиг — `hugo.toml [params.page.comment.giscus]`. Valine/LeanCloud отключены (LeanCloud international закрывается 12.01.2027).

## Поиск

Клиентский Lunr.js: индекс `/index.json` (и `/ru/index.json`) генерируется при сборке, поиск выполняется в браузере, включая русский стемминг. Внешних сервисов нет.
