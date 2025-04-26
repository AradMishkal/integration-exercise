class InventoryUnit
  include Mongoid::Document
  include Mongoid::Timestamps

  field :name, type: String
  field :quantity, type: Integer
  field :price, type: Float
  field :batch_id, type: String
end
