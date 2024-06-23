class UnsupportedPlatformError(Exception):
	def __init__(self, platform_name: str):
		super().__init__(f"The '{platform_name}' platform is not supported")
