from django.urls import path

from web.views import (
    DriveDetail,
    CarDriveEdit,
    AnalysisCreate,
    CarDriveFileList,
    DataFileDetail,
    CarTypeList,
)

urlpatterns = [
    path("", DataFileDetail.as_view(), name="file_detail"),
    path("analysis/create", AnalysisCreate.as_view(), name="analysis_create"),
    path("cars", CarDriveFileList.as_view(), name="cars_file_detail"),
    path("cartypes", CarTypeList.as_view(), name="cars_types_list"),
    path("car/<int:pk>", CarDriveEdit.as_view(), name="cars_file_update"),
    path("drive/<int:pk>", DriveDetail.as_view(), name="drive_detail"),
]
