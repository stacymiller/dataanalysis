c = get_config()
c.NbConvertApp.export_format = 'pdf'
c.TemplateExporter.template_path = ['./templates']
c.Exporter.template_file = 'russian_article'
