class InventoryUnit
  include Mongoid::Document
  include Mongoid::Timestamps
# Fields for each inventory unit
  field :name, type: String
  field :quantity, type: Integer
  field :price, type: Float
  field :batch_id, type: String
# Validate that all fields are present
  validates :name, :quantity, :price, :batch_id, presence: true
end