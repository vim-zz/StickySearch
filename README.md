# StickySearch

A Sublime Text plugin - persistently highlighting selected text. This plugin is designed
to elevate your text highlighting experience, drawing inspiration from VIM's keyword search functionality.

Compatible with Sublime Text 3 and 4.

<img width="822" alt="Screenshot 2023-08-18 at 17 52 53" src="https://github.com/vim-zz/StickySearch/assets/50141/74d6744b-8f53-4b90-9396-d7e44d280970">

## How It Works

To highlight text under the cursor:

- macOS: `Command + 8`
- Windows/Linux: `Ctrl + 8`

To highlight more text (while retaining previous highlights):

- macOS: Shift + `Command + 8`
- Windows/Linux: `Shift + Ctrl + 8`

To clear all highlighted text:

- macOS: Alt + `Command + 8`
- Windows/Linux: `Alt + Ctrl + 8`

## Customization

You can change the following settings:

| Parameter | Values                              | Description                                         |
|-----------|-------------------------------------|-----------------------------------------------------|
| `icon`    | `dot`, `circle`, `bookmark`, `cross`| When provided, the named icon will be displayed in the gutter |
| `fill`    | `true`, `false`                     | When set to `true`, it adds a background color to marked text |
| `outline` | `true`, `false`                     | When set to `true`, it encloses marked text with a colored frame |
| `rainbow` | `true`, `false`                     | When set to `true`, different colors are used for each added selection |
