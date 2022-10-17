username = models.CharField(max_length=30)
password = models.CharField(max_length=30)
additional_info = models.CharField(max_length=255)
isMovedToExtDB = models.BooleanField(default=False)
student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='db_accounts')
editionServer = models.ForeignKey(EditionServer, on_delete=models.SET_NULL, null=True)

