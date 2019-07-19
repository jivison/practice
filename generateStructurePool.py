def parse(component):
    partConversions = {
        "object" : ["noun", "object"],
        "subject" : ["noun", "subject"],
        "verb" : ["verb"],
        "adjective" : ["adjective"],
        "determiner" : ["determiner"]
    }

    callbackConversion = {
        "places" : "timeplace",
        "time" : "timeplace"
    }

    main = None
    options = None

    callback = None
    topic = None

    if ":" in component:
        options = {}
        main, c, modifier = component.partition(":")

        main = [main]

        if "(" in modifier:
            callback = modifier
            topic = None
        else:
            callback = None
            topic = modifier
        
    else:
        main = partConversions[component]

    if callback:
        function, params = callback.split("(")
        params = params.replace(")", "")
        options["callback"] = {"name" : function, "params" : params.split("|")}

    if topic:
        options["filter"] = topic
        if main[0] == "noun": 
            options["callback"] = {"name" : callbackConversion[topic]}

    return main, options

    

def generate():
    with open("structures", "r") as structureFile:
        
        structures = []
        
        for line in structureFile:
            if line[0] != "#":
                components = line.strip().split(" ")

                structureComponents = []

                for component in components:
                    speechPart, options = parse(component)
                    structureComponent = {"speechPart" : speechPart, "options" : options}
                    structureComponents.append(structureComponent)

                structures.append(structureComponents)

    return structures