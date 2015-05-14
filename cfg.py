c = get_config()
c.Application.verbose_crash=True
c.NbConvertApp.export_format = 'pdf'
# c.NbConvertApp.postprocessor_class = 'pdf'

c.Exporter.template_file = 'russian-article.tplx'
