let
mkLiteral = value: {
      _type = "literal";
      inherit value;
};
bg = mkLiteral "#1a1b26cc";
fg = mkLiteral "#a0b1d6";
active = mkLiteral "#1a1b26";
in {
    "*"= {
        font = "Caskaydia Cove Nerd Font 13";
        text-color = fg;
        background-color = mkLiteral "#00000000";
    };

    "window" = {
        padding = 10;
        background-color = bg;
        border = 10;
    };

    "inputbar" = {
    };

    "element.selected" = {
        background-color = active;
    };
}
