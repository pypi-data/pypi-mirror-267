"""
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
"""


import json
import re
from typing import ClassVar, Dict, Optional, Tuple, Union
from dataclasses import dataclass
from argparse import Namespace

from mkdocs.exceptions import BuildError


from pyodide_mkdocs_theme.pyodide_macros.plugin.maestro_tools import dump_and_dumper


@dataclass
class JsDumper:
    # pylint: disable=no-member

    PROPS: ClassVar[Tuple[str]] = tuple('msg plural em as_pattern kbd'.split())

    def __str__(self):
        return self.msg

    def dump_as_dct(self):
        dct = {
            prop: v for prop in self.PROPS if (v := self.get_prop(prop)) is not None
        }
        return dct


    def get_prop(self,prop):
        return str(self) if prop=='msg' else getattr(self, prop, None)



@dataclass
class Msg(JsDumper):
    msg: str



@dataclass
class MsgPlural(Msg):
    plural: str = ''

    def __post_init__(self):
        self.plural = self.plural or self.msg+'s'

    def one_or_many(self, many:bool):
        return self.plural if many else self.msg



@dataclass
class TestsToken(JsDumper):
    msg: str
    as_pattern = re.compile('')       # Overridden in post_init. Needed for types in 3.8

    def __post_init__(self):
        s = self.msg.strip()
        short = s.replace(' ','').lower()

        if not s.startswith('#'):
            raise BuildError(
                "The public tests token must start with '#'"
            )
        if '\n' in s:
            raise BuildError(
                "The public tests token should use a single line"
                " (ignoring leading or trailing new lines)"
            )
        if short=='#test' or len(short)<6:
            raise BuildError(
                "The public tests token is too short/simple and could cause false positives."
                " Use at least something like '# Tests', or something longer."
            )

        pattern = re.sub(r'\s+', r"\\s*", s)
        self.as_pattern = re.compile(pattern, flags=re.I)

    def __str__(self):
        return self.msg.strip()

    def get_prop(self,prop):
        return self.as_pattern.pattern if prop=='as_pattern' else super().get_prop(prop)




@dataclass
class Tip(JsDumper):
    em: int                     # Width, in em. If 0, use automatic width
    msg: str                    # tooltip message
    kbd: Optional[str] = ""     # ex: "Ctrl+I" / WARNING: DO NOT MODIFY DEFAULTS!

    def __str__(self):
        if not self.kbd:
            return self.msg

        kbd = re.sub(r"(\w+)", r"<kbd>\1</kbd>", self.kbd)
        msg = f"{ self.msg }<br>({ kbd })"
        return msg






Tr = Union[Msg, MsgPlural, Tip, TestsToken]
LangProp = str



class Lang(Namespace):
    # pylint: disable=no-member

    #infos:
    success_msg:   Tr = Msg("Terminé sans erreur !")
    run_script:    Tr = Msg("Script lancé...")
    install_start: Tr = Msg("Installation de certains paquets. Ceci peut prendre un certain temps...")
    install_done:  Tr = Msg("Installations terminées!")

    # QCMS:
    qcm_title:  Tr = MsgPlural("Question")

    # IDEs:
    tests:      Tr = TestsToken("\n\n# Tests\n\n")

    title_corr: Tr = Msg('Solution')
    title_rem:  Tr = Msg('Remarques')

    corr:       Tr = Msg('🐍 Proposition de correction')
    rem:        Tr = Msg('Remarques')

    play:       Tr = Tip(9,  "Exécuter le code", "Ctrl+S")
    check:      Tr = Tip(9,  "Valider", "Ctrl+Enter")
    download:   Tr = Tip(0,  "Télécharger")
    upload:     Tr = Tip(0,  "Téléverser")
    restart:    Tr = Tip(0,  "Réinitialiser l'éditeur")
    save:       Tr = Tip(0,  "Sauvegarder dans le navigateur")
    comments:   Tr = Tip(15, "(Dés-)Active le code après la ligne <code>{tests}</code> "
                             "(insensible à la casse)", "Ctrl+I")
    feedback:   Tr = Tip(15,  "Tronquer ou non le feedback dans les terminaux (sortie standard & stacktrace / relancer le code pour appliquer)")

    #terminals:
    success_head:  Tr = Msg("Bravo !")
    success_head_xtra: Tr = Msg("Pensez à lire")
    fail_head:     Tr = Msg("Dommage !")

    reveal_corr:   Tr = Msg("le corrigé")
    reveal_join:   Tr = Msg("et")
    reveal_rem:    Tr = Msg("les commentaires")

    success_tail:  Tr = Msg("Vous avez réussi tous les tests !")
    fail_tail:     Tr = Msg("est maintenant disponible")
    fail_tail_plural: Tr = Msg("sont maintenant disponibles")


    #Other buttons tooltips:
    tip_trash:     Tr = Tip(15, "Supprimer tous les codes enregistrés sur ce navigateur")
    tip_qcm_mask:  Tr = Tip(15, "Les réponses resteront cachées...")
    tip_qcm_check: Tr = Tip(11, "Vérifier les réponses")
    tip_qcm_redo:  Tr = Tip(9,  "Recommencer")





    #-------------------------------------------------------------------------



    def overload(self, dct: Dict[LangProp,Tr]):
        """
        Overloads the defaults with any available user config data.
        This has to be done at macro registration time.
        """
        for k,v in dct:
            current = getattr(self,k, None)

            if current is None:
                raise BuildError(f"Invalid Lang property: {k!r}")
            if not isinstance(v, current.__class__):
                kls = current.__class__.__name__
                raise BuildError(f"Invalid Translation type: {v!r} should be an instance of {kls}")
            setattr(self,k,v)



    @classmethod
    def dump_as_str(cls, obj=None):
        """
        Create a complete json object with all teh string representations of all the messages.
        - Takes potential overloads in consideration
        - WARNING: js dumps are simple str conversions, so far, so some messages might be
                   missing some information... (specifically, plurals)
        - If obj is None, use null for all values.
        """
        dct = dump_and_dumper(cls.__annotations__, obj, lambda v: v.dump_as_dct() if v else "null")
        if obj:
            return json.dumps(dct)

        return json.dumps(dct, indent=8).replace('"','')
