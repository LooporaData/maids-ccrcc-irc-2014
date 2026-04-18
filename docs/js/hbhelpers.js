Handlebars.registerHelper("ifUnanswered", function() {
    if (this.entry.answer === "" || this.entry.answer === "None") {
        return new Handlebars.SafeString('<span style="color:red;">(Unanswered)</span>')
    } else {
        return ""
    }
})

Handlebars.registerHelper("addLinkSubset", function() {
    if (this.subset.link !== "" && this.subset.link.toLowerCase() !== "none") {
        return new Handlebars.SafeString(`<a href="${this.subset.link}">External documentation</a>`)
    } else {
        return "No external documentation."
    }
})

Handlebars.registerHelper("addLinkDefinition", function() {
    if (this.definition.link !== "" && this.definition.link.toLowerCase() !== "none") {
        return new Handlebars.SafeString(` (<a href="${this.definition.link}">link</a>)`)
    } else {
        return ""
    }
})