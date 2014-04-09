'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import sys
import xbmc
import utils
from xbmcgui import Dialog
from editor import Editor
from utils import tr


if __name__ == "__main__":
    ## load mappings ##
    default = xbmc.translatePath('special://xbmc/system/keymaps/keyboard.xml')
    userdata = xbmc.translatePath('special://userdata/keymaps')
    gen_file = os.path.join(userdata, 'gen.xml')

    if not os.path.exists(userdata):
        os.makedirs(userdata)
    else:
        #make sure there are no user defined keymaps
        for name in os.listdir(userdata):
            if name.endswith('.xml'):
                if name != os.path.basename(gen_file):
                    src = os.path.join(userdata, name)
                    dst = os.path.join(userdata, name + ".bak")
                    os.rename(src, dst)
    defaultkeymap = utils.read_keymap(default)
    userkeymap = utils.read_keymap(gen_file) if os.path.exists(gen_file) else []

    ## main loop ##
    confirm_discard = False
    while True:
        idx = Dialog().select(tr(30000), [tr(30003), tr(30004), tr(30005)])
        if idx == 0:
            # edit
            editor = Editor(defaultkeymap, userkeymap)
            editor.start()
            confirm_discard = editor.dirty
        elif idx == 1:
            # reset
            confirm_discard = bool(userkeymap)
            userkeymap = []
        elif idx == 2:
            # save
            if os.path.exists(gen_file):
                os.rename(gen_file, gen_file + ".old")
            utils.write_keymap(userkeymap, gen_file)
            xbmc.executebuiltin("action(reloadkeymaps)")
            break
        elif idx == -1 and confirm_discard:
            if Dialog().yesno(tr(30000), tr(30006)) == 1:
                break
        else:
            break

    sys.modules.clear()