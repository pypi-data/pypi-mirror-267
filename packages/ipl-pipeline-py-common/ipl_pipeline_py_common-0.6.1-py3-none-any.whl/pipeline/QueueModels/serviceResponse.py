from pydantic import BaseModel, Field, model_validator
from typing import Optional, Generic, TypeVar

T = TypeVar("T", bound=BaseModel)


class ServiceResponse(BaseModel, Generic[T]):
    response_node_id: Optional[str] = Field("unknown")
    response_node_version: Optional[str] = Field("unknown")
    request_error: bool = Field(False, description="Error in request")
    request_error_message: Optional[str] = Field(None, description="Error Message")
    response_data: Optional[T] = Field(None, description="Response Data")

    @model_validator(mode='after')
    def check_state(self):
        """
        Check if response data is None if request error is True
        :return:
        """
        if self.request_error and self.response_data:
            raise ValueError("Response data should be None if request error is True")
        return self
