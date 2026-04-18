from helperHandlebars import getHTML, getFIGURES
import bs4,argparse,os,shutil

parser = argparse.ArgumentParser(prog="xml2html.py", description = "Convert XML to index.html with a handlebars data object.")
parser.add_argument("-u", "--use", type=str, help="Name a directory within ./xml/ that contains prefilled XML descriptions.")
parser.add_argument("-t", "--template", type=str, default="maids", help="Name a compiled handlebars template named within ./docs/js/hbmaids.js.")
args = parser.parse_args()

egDir = ""
if (args.use): egDir = "/{}".format(args.use)

with open("./code/templates/maids.html") as f:
    template = f.read()

html = {
    "about"         : getHTML(f"./xml{egDir}/about.xml"               , "ABOUT"),
    "provenance"    : getHTML(f"./xml{egDir}/version_provenance.xml"  , "PROVENANCE"),
    "questionnaire" : getHTML(f"./xml{egDir}/questionnaire.xml"       , "QUESTIONNAIRE"),
    "definitions"   : getHTML(f"./xml{egDir}/keyword_definitions.xml" , "DEFINITION"),
    "subsets"       : getHTML(f"./xml{egDir}/feature_description.xml" , "FEATURE")
}

with open("./docs/index.html", 'w') as o:    
    handleFunction  = "var filledHandle = template({{ {ABOUT},{PROVENANCE},categories:[{QUESTIONNAIRE}],definitions:[{DEFINITIONS}],subsets:[{SUBSETS}] }})".format(
        ABOUT          = html["about"],
        PROVENANCE     = html["provenance"],
        QUESTIONNAIRE  = html["questionnaire"],
        DEFINITIONS    = html["definitions"],
        SUBSETS        = html["subsets"]
    )
    root = template.format(PUT_TEMPLATE_HERE = args.template, PUT_HANDLE_HERE = handleFunction)
    root = bs4.BeautifulSoup(root, "html.parser")
    o.write(root.prettify())

msg = ""
for fName in getFIGURES(f"./xml{egDir}/about.xml"):
    copyFrom = f"./supplementary/figures/{fName}"
    copyTo   = f"./docs/images/figures/{fName}"
    if os.path.isfile(copyFrom):
        shutil.copyfile(copyFrom, copyTo)
    else:
        msg += f"  * {fName}\n"

if len(msg) != 0:
    msg = f"Could not find the following figures in './supplementary/figures/':\n{msg}"
    print (f"{msg}\nThis is expected if -u example is used." if args.use == "example" else msg)