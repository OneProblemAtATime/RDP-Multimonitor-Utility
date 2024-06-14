import xml.dom.minidom

def main():
    doc = xml.dom.minidom.parse("samplexml.xml")
    print(doc.nodeName)
    print(doc.firstChild.tagName)
    skills = doc.getElementsByTagName("skill")
    print(skills.length)
    for i in skills:
        print(i.getAttribute("name"))

    newSkill = doc.createElement("skill")
    newSkill.setAttribute("name", "jQuery")
    doc.firstChild.appendChild(newSkill)
    print("---")
    skills = doc.getElementsByTagName("skill")
    for i in skills:
        print(i.getAttribute("name"))

    # Save the modified XML back to the same file
    with open("samplexml.xml", "w") as file:
        doc.writexml(file, addindent="")



if __name__ == "__main__":
    main()