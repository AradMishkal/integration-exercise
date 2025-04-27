class InventoryUnit
  include Mongoid::Document
  include Mongoid::Timestamps
# Define fields for the inventory unit
  field :name, type: String
  field :quantity, type: Integer
  field :price, type: Float
  field :batch_id, type: String

  validates :name, :quantity, :price, :batch_id, presence: true
end