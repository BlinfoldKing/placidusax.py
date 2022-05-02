{ config, lib, pkgs, ... }:

with lib;

let
  cfg = config.services.xserver.windowManager.placidusax;
in
{
  
  options.services.xserver.windowManager.placidusax = {
    enable = mkEnableOption "placidusax";
    wallpaper = mkOption {
        type = types.str;
    };
    package = mkPackageOption pkgs "qtile" { };
  };

  config = mkIf cfg.enable {
    services.xserver.windowManager.session = [{
      name = "placidusax";
      start = ''
        chmod +x /etc/nixos/qtile/rofi-wifi-menu.sh &
        eww -c /etc/nixos/qtile/eww daemon &
        eww -c /etc/nixos/qtile/eww open bar &
        nitrogen --set-zoom-fill ${cfg.wallpaper} &
        ${cfg.package}/bin/qtile start -c /etc/nixos/qtile/config.py &
        waitPID=$!
      '';
    }];

    environment.systemPackages = [
      # pkgs.qtile is currently a buildenv of qtile and its dependencies.
      # For userland commands, we want the underlying package so that
      # packages such as python don't bleed into userland and overwrite intended behavior.
      (cfg.package.unwrapped or cfg.package)
    ];
  };
}
